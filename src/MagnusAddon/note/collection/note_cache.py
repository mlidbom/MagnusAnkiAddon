from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.jpnote import JPNote
from qt_utils.task_runner_progress_dialog import TaskRunner
from sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from sysutils.typed import checked_cast
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner

class CachedNote(Slots):
    def __init__(self, note: JPNote) -> None:
        self.id: NoteId = note.get_id()
        self.question: str = note.get_question()

class NoteCache[TNote: JPNote, TSnapshot: CachedNote](Slots):
    def __init__(self, all_notes: list[TNote], cached_note_type: type[TNote], cache_runner: CacheRunner) -> None:
        self._note_type: type[TNote] = cached_note_type
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_question: DefaultDictCaseInsensitive[QList[TNote]] = DefaultDictCaseInsensitive(QList[TNote])
        self._by_id: dict[NoteId, TNote] = {}
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}

        self._deleted: QSet[NoteId] = QSet()

        self._flushing: bool = False
        self._pending_add: list[Note] = []

        if len(all_notes) > 0:
            with TaskRunner.current(f"Pushing {all_notes[0].__class__.__name__} notes into cache") as task_runner:
                task_runner.process_with_progress(all_notes, self.add_note_to_cache, f"Pushing {all_notes[0].__class__.__name__} notes into cache")

        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_note_addded(self._on_added)
        cache_runner.connect_will_flush(self._on_will_flush)

    def all(self) -> QList[TNote]:
        return QList(self._by_id.values())

    def with_id_or_none(self, note_id: NoteId) -> TNote | None:
        return self._by_id.get(note_id, None)

    def with_question(self, question: str) -> QList[TNote]:
        return self._by_question.get_value_or_default(question).to_list()

    def _create_snapshot(self, note: TNote) -> TSnapshot: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_remove_from_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]
    def _inheritor_add_to_cache(self, note: TNote, snapshot: TSnapshot) -> None: raise NotImplementedError()  # pyright: ignore[reportUnusedParameter]

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

    def _on_added(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self.add_note_to_cache(note)

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
        self._inheritor_remove_from_cache(note, cached)

    def add_note_to_cache(self, note: TNote) -> None:
        if note.get_id() in self._by_id: return
        assert note.get_id()
        self._by_id[note.get_id()] = note
        snapshot = self._create_snapshot(note)
        self._snapshot_by_id[note.get_id()] = snapshot
        self._by_question[note.get_question()].append(note)
        self._inheritor_add_to_cache(note, snapshot)
