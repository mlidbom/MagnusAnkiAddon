from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots
from line_profiling_hacks import profile_lines
from note.jpnote import JPNote
from sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from sysutils.collections.queryable.q_iterable import QList
from sysutils.typed import checked_cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner
    from qt_utils.task_runner_progress_dialog import ITaskRunner

class CachedNote(AutoSlots):
    def __init__(self, note: JPNote) -> None:
        self.id: NoteId = note.get_id()
        self.answer: str = note.get_answer()
        self.question: str = note.get_question()

class NoteCache[TNote: JPNote, TSnapshot: CachedNote](AutoSlots):
    @profile_lines
    def __init__(self, all_notes: list[TNote], cached_note_type: type[TNote], cache_runner: CacheRunner, task_runner: ITaskRunner) -> None:
        self._note_type: type[TNote] = cached_note_type
        self._by_question: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)
        self._by_id: dict[NoteId, TNote] = {}
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}
        self._by_answer: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)

        self._deleted: set[NoteId] = set()

        self._flushing: bool = False
        self._pending_add: list[Note] = []

        if len(all_notes) > 0:
            task_runner.process_with_progress(all_notes, self.add_note_to_cache, f"Pushing {all_notes[0].__class__.__name__} notes into cache")

        cache_runner.connect_merge_pending_adds(self._merge_pending_added_notes)
        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_will_add(self._on_will_be_added)
        cache_runner.connect_will_flush(self._on_will_flush)

    def all(self) -> QList[TNote]:
        return QList(self._by_id.values())

    def with_id_or_none(self, note_id: NoteId) -> TNote | None:
        return self._by_id.get(note_id, None)

    def with_question(self, question: str) -> QList[TNote]:
        return QList(self._by_question[question])

    def _create_snapshot(self, note: TNote) -> TSnapshot: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_remove_from_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_add_to_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

    def _merge_pending_added_notes(self) -> None:
        completely_added_list = [pending for pending in self._pending_add if pending.id]
        for backend_note in completely_added_list:
            self._pending_add.remove(backend_note)
            note = checked_cast(self._note_type, JPNote.note_from_note(backend_note))
            self.add_note_to_cache(note)

    def _on_will_flush(self, backend_note: Note) -> None:
        if backend_note.id and backend_note.id in self._by_id:
            cached_note = self._by_id[backend_note.id]

            if cached_note.is_flushing:  # our code called flush, we should just make sure the cached data is up to date
                self._refresh_in_cache(cached_note)
            else:  # a note has been edited outside of our control, we need to switch to that up-to-date note and refresh generated data
                note = self._create_note(backend_note)
                with note.recursive_flush_guard.pause_flushing():
                    note.update_generated_data()
                    self._refresh_in_cache(note)
        elif backend_note.id in self._deleted:  # undeleted note
            self._deleted.remove(backend_note.id)
            note = self._create_note(backend_note)
            with note.recursive_flush_guard.pause_flushing():
                note.update_generated_data()
                self.add_note_to_cache(note)

    def _on_will_be_added(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self._pending_add.append(backend_note)

    def _on_will_be_removed(self, note_ids: Sequence[NoteId]) -> None:
        my_notes_ids = [note_id for note_id in note_ids if note_id in self._by_id]
        cached_notes = [self._by_id[note_id] for note_id in my_notes_ids]
        self._deleted.update(my_notes_ids)
        for cached in cached_notes:
            self._remove_from_cache(cached)

    def _create_note(self, backend_note: Note) -> TNote:
        return checked_cast(self._note_type, JPNote.note_from_note(backend_note))

    def _refresh_in_cache(self, note: TNote) -> None:
        self._remove_from_cache(note)
        self.add_note_to_cache(note)

    def _remove_from_cache(self, note: TNote) -> None:
        assert note.get_id()
        cached = self._snapshot_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].remove(note)
        self._by_answer[cached.answer].remove(note)
        self._inheritor_remove_from_cache(note, cached)

    def add_note_to_cache(self, note: TNote) -> None:
        assert note.get_id()
        self._by_id[note.get_id()] = note
        snapshot = self._create_snapshot(note)
        self._snapshot_by_id[note.get_id()] = snapshot
        self._by_question[note.get_question()].add(note)
        self._by_answer[note.get_answer()].add(note)
        self._inheritor_add_to_cache(note, snapshot)
