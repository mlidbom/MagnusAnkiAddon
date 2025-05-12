from __future__ import annotations

import time
from dataclasses import dataclass
from queue import Queue
from threading import Event, Thread
from typing import TYPE_CHECKING, Callable, cast

from anki import hooks
from anki.models import ModelManager, NotetypeDict
from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from note.note_constants import NoteTypes
from sysutils import app_thread_pool
from sysutils.typed import checked_cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.collection import Collection
    from anki.decks import DeckId
    from anki.notes import Note, NoteId

@dataclass
class Task:
    func: Callable[[], None]
    completion_event: Event | None = None

class DedicatedThread:
    def __init__(self) -> None:
        self.queue: Queue[Task] = Queue()
        self.thread: Thread = Thread(target=self._worker, daemon=True)
        self._running = True
        self.thread.start()

    def _worker(self) -> None:
        while self._running:
            task: Task = self.queue.get()
            task.func()
            if task.completion_event is not None:
                task.completion_event.set()
            self.queue.task_done()

    def submit(self, task: Callable[[], None], wait: bool = False) -> None:
        completion_event = Event() if wait else None
        self.queue.put(Task(task, completion_event))
        if wait:
            completion_event.wait()  # type: ignore

    def destruct(self) -> None:
        self._running = False

        def null_op() -> None:
            pass
        self.submit(null_op)  # Prevents deadlock
        self.thread.join()

class CacheRunner:
    def __init__(self, anki_collection: Collection) -> None:
        self._pause_data_generation: bool = False
        self._generate_data_subscribers: list[Callable[[], None]] = []
        self._merge_pending_subscribers: list[Callable[[], None]] = []
        self._will_add_subscribers: list[Callable[[Note], None]] = []
        self._will_flush_subscribers: list[Callable[[Note], None]] = []
        self._will_remove_subscribers: list[Callable[[Sequence[NoteId]], None]] = []
        self._destructors: list[Callable[[], None]] = []
        self._anki_collection: Collection = anki_collection
        self._dedicated_thread: DedicatedThread = DedicatedThread()
        self._running: bool = False

        model_manager: ModelManager = anki_collection.models
        all_note_types: list[NoteTypeEx] = [NoteTypeEx.from_dict(model) for model in model_manager.all()]
        self._note_types: list[NoteTypeEx] = [note_type for note_type in all_note_types if note_type.name in NoteTypes.ALL]
        assert len(self._note_types) == len(NoteTypes.ALL)

        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_be_added.append(self._on_will_be_added)
        hooks.note_will_flush.append(self._on_will_flush)

    def start(self) -> None:
        assert not self._running
        self._running = True
        app_thread_pool.pool.submit(self._run_periodic_flushes)

    def _run_periodic_flushes(self) -> None:
        while self._running:
            self.flush_updates()
            time.sleep(0.1)

    def destruct(self) -> None:
        self._running = False
        self._dedicated_thread.destruct()
        self._internal_flush_updates()

        hooks.notes_will_be_deleted.remove(self._on_will_be_removed)
        hooks.note_will_be_added.remove(self._on_will_be_added)
        hooks.note_will_flush.remove(self._on_will_flush)

        for destructor in self._destructors: destructor()

        from note import noteutils
        noteutils.clear_studying_cache()

    def _internal_flush_updates(self) -> None:
        self._check_for_updated_note_types_and_reset_app_if_found()
        for subscriber in self._merge_pending_subscribers: subscriber()

        if self._pause_data_generation: return
        for callback in self._generate_data_subscribers: callback()

    def flush_updates(self) -> None:
        self._dedicated_thread.submit(self._internal_flush_updates, wait=True)

    def _on_will_be_added(self, _collection: Collection, backend_note: Note, _deck_id: DeckId) -> None:
        def task() -> None:
            for subscriber in self._will_add_subscribers: subscriber(backend_note)

        self._dedicated_thread.submit(task)

    def _on_will_flush(self, backend_note: Note) -> None:
        def task() -> None:
            for subscriber in self._will_flush_subscribers: subscriber(backend_note)

        self._dedicated_thread.submit(task)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        def task() -> None:
            for subscriber in self._will_remove_subscribers: subscriber(note_ids)

        self._dedicated_thread.submit(task)

    def pause_data_generation(self) -> None:
        assert not self._pause_data_generation
        self._pause_data_generation = True

    def resume_data_generation(self) -> None:
        assert self._pause_data_generation
        self._pause_data_generation = False

    def connect_generate_data_timer(self, flush_updates: Callable[[], None]) -> None:
        self._generate_data_subscribers.append(flush_updates)

    def connect_merge_pending_adds(self, _merge_pending_added_notes: Callable[[], None]) -> None:
        self._merge_pending_subscribers.append(_merge_pending_added_notes)

    def connect_will_add(self, _merge_pending_added_notes: Callable[[Note], None]) -> None:
        self._will_add_subscribers.append(_merge_pending_added_notes)

    def connect_will_flush(self, _merge_pending_added_notes: Callable[[Note], None]) -> None:
        self._will_flush_subscribers.append(_merge_pending_added_notes)

    def connect_will_remove(self, _merge_pending_added_notes: Callable[[Sequence[NoteId]], None]) -> None:
        self._will_remove_subscribers.append(_merge_pending_added_notes)

    def _check_for_updated_note_types_and_reset_app_if_found(self) -> None:
        for cached_note_type in self._note_types:
            assert self._anki_collection.db
            current = NoteTypeEx.from_dict(cast(NotetypeDict, checked_cast(ModelManager, self._anki_collection.models).get(cached_note_type.id)))
            try:
                current.assert_schema_matches(cached_note_type)
            except AssertionError:
                from ankiutils import app
                app.reset()
