from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from autoslot import Slots
from note.jpnote import JPNote
from sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from sysutils.timeutil import StopWatch
from sysutils.typed import checked_cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner

class CachedNote(Slots):
    def __init__(self, note: JPNote) -> None:
        self.id = note.get_id()
        self.answer = note.get_answer()
        self.question = note.get_question()

TNote = TypeVar("TNote", bound=JPNote)
TSnapshot = TypeVar("TSnapshot", bound=CachedNote)

class NoteCache(Generic[TNote, TSnapshot], Slots):
    def __init__(self, all_notes: list[TNote], cached_note_type: type[TNote], cache_runner: CacheRunner) -> None:
        self._note_type = cached_note_type
        self._by_question: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)
        self._by_id: dict[NoteId, TNote] = {}
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}
        self._by_answer: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)

        self._deleted: set[NoteId] = set()

        self._flushing = False
        self._pending_add: list[Note] = []

        with StopWatch.log_execution_time(f"pushing {cached_note_type.__name__}s into cache"):
            for _note in all_notes:
                self._add_to_cache(_note)

        cache_runner.connect_merge_pending_adds(self._merge_pending_added_notes)
        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_will_add(self._on_will_be_added)
        cache_runner.connect_will_flush(self._on_will_flush)

    def all(self) -> list[TNote]:
        return list(self._by_id.values())

    def with_id_or_none(self, note_id: NoteId) -> TNote | None:
        return self._by_id.get(note_id, None)

    def with_question(self, question: str) -> list[TNote]:
        return list(self._by_question[question])

    @abstractmethod
    def _create_snapshot(self, note: TNote) -> TSnapshot: pass
    def _inheritor_remove_from_cache(self, note: TNote, cached: TSnapshot) -> None: pass
    def _inheritor_add_to_cache(self, note: TNote) -> None: pass

    def _merge_pending_added_notes(self) -> None:
        completely_added_list = [pending for pending in self._pending_add if pending.id]
        for backend_note in completely_added_list:
            self._pending_add.remove(backend_note)
            note = checked_cast(self._note_type, JPNote.note_from_note(backend_note))
            self._add_to_cache(note)

    def _on_will_flush(self, backend_note: Note) -> None:
        if backend_note.id and backend_note.id in self._by_id:
            cached_note = self._by_id[backend_note.id]

            if cached_note.is_flushing:  # our code called flush, we should just make sure the cached data is up to date
                self._refresh_in_cache(cached_note)
            else:  # a note has been edited outside of our control, we need to switch to that up-to-date note and refresh generated data
                note = self._create_note(backend_note)
                with note.flush_guard.pause_flushing():
                    note.update_generated_data()
                    self._refresh_in_cache(note)
        elif backend_note.id in self._deleted:  # undeleted note
            self._deleted.remove(backend_note.id)
            note = self._create_note(backend_note)
            with note.flush_guard.pause_flushing():
                note.update_generated_data()
                self._add_to_cache(note)

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
        self._add_to_cache(note)

    def _remove_from_cache(self, note: TNote) -> None:
        assert note.get_id()
        cached = self._snapshot_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].remove(note)
        self._by_answer[cached.answer].remove(note)
        self._inheritor_remove_from_cache(note, cached)

    def _add_to_cache(self, note: TNote) -> None:
        assert note.get_id()
        self._by_id[note.get_id()] = note
        self._snapshot_by_id[note.get_id()] = self._create_snapshot(note)
        self._by_question[note.get_question()].add(note)
        self._by_answer[note.get_answer()].add(note)
        self._inheritor_add_to_cache(note)
