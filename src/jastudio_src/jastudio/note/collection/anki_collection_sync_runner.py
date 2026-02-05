from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from anki import hooks
from anki.models import ModelManager
from autoslot import Slots
from jaspythonutils.sysutils import ex_assert
from jaspythonutils.sysutils.typed import checked_cast, non_optional
from jastudio.anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from jastudio.ankiutils import app
from JAStudio.Core.Note import NoteTypes
from jastudio.sysutils import app_thread_pool, ex_thread
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from anki.collection import Collection
    from anki.decks import DeckId
    from anki.notes import Note, NoteId

class AnkiCollectionSyncRunner(Slots):
    def __init__(self, anki_collection: Collection) -> None:
        self._merge_pending_subscribers: list[Callable[[], None]] = []
        self._added_subscribers: list[Callable[[Note], None]] = []
        self._will_flush_subscribers: list[Callable[[Note], None]] = []
        self._will_remove_subscribers: list[Callable[[Sequence[NoteId]], None]] = []
        self._destructors: list[Callable[[], None]] = []
        self._anki_collection: Collection = anki_collection
        self._running: bool = False
        self._lock: threading.RLock = threading.RLock()

        self._pending_add: QList[Note] = QList()

        model_manager: ModelManager = anki_collection.models
        all_note_types: list[NoteTypeEx] = [NoteTypeEx.from_dict(model) for model in model_manager.all()]
        self._note_types: list[NoteTypeEx] = [note_type for note_type in all_note_types if note_type.name in NoteTypes.ALL]
        ex_assert.equal(len(self._note_types), len(NoteTypes.ALL))

        hooks.notes_will_be_deleted.append(self._on_will_be_removed)  # pyright: ignore[reportUnknownMemberType]
        hooks.note_will_be_added.append(self._on_will_be_added)  # pyright: ignore[reportUnknownMemberType]
        hooks.note_will_flush.append(self._on_will_flush)

    def start(self) -> None:
        with self._lock:
            ex_assert.that(not self._running)
            self._running = True
            app_thread_pool.pool.submit(self._run_periodic_flushes)

    def _run_periodic_flushes(self) -> None:
        while self._running:
            self.flush_updates()
            ex_thread.sleep_thread_not_doing_the_current_work(0.1)
    #
    def destruct(self) -> None:
        with self._lock:
            self._running = False
            self._internal_flush_updates()

            hooks.notes_will_be_deleted.remove(self._on_will_be_removed)  # pyright: ignore[reportUnknownMemberType]
            hooks.note_will_be_added.remove(self._on_will_be_added)  # pyright: ignore[reportUnknownMemberType]
            hooks.note_will_flush.remove(self._on_will_flush)

            for destructor in self._destructors: destructor()

    def _internal_flush_updates(self) -> None:
        completely_added_list = self._pending_add.where(lambda it: it.id != 0).to_list()
        self._pending_add = self._pending_add.where(lambda it: it.id == 0).to_list()
        for note in completely_added_list:
            for subscriber in self._added_subscribers: subscriber(note)

    def flush_updates(self) -> None:
        with self._lock:
            self._check_for_updated_note_types_and_reset_app_if_found()
            self._internal_flush_updates()

    def _on_will_be_added(self, _collection: Collection, backend_note: Note, _deck_id: DeckId) -> None:  # pyright: ignore[reportUnusedParameter]
        if not self._running: return
        with self._lock:
            self._pending_add.append(backend_note)

    def _on_will_flush(self, backend_note: Note) -> None:
        if not self._running: return
        with self._lock:
            for subscriber in self._will_flush_subscribers: subscriber(backend_note)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        if not self._running: return
        with self._lock:
            for callback in self._will_remove_subscribers: callback(note_ids)

    def connect_note_addded(self, on_added: Callable[[Note], None]) -> None:
        with self._lock:
            self._added_subscribers.append(on_added)

    def connect_will_flush(self, on_will_flush: Callable[[Note], None]) -> None:
        with self._lock:
            self._will_flush_subscribers.append(on_will_flush)

    def connect_will_remove(self, on_will_remove: Callable[[Sequence[NoteId]], None]) -> None:
        with self._lock:
            self._will_remove_subscribers.append(on_will_remove)

    def _check_for_updated_note_types_and_reset_app_if_found(self) -> None:
        for cached_note_type in self._note_types:
            ex_assert.not_none(self._anki_collection.db)
            current = NoteTypeEx.from_dict(non_optional(checked_cast(ModelManager, self._anki_collection.models).get(cached_note_type.id)))
            try:
                current.assert_schema_matches(cached_note_type)
            except AssertionError:
                app_thread_pool.pool.submit(lambda: app.reset())  # We are running on the thread that will be killed by the reset...
