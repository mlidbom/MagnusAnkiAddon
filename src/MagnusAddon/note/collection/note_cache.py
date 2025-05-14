from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from note.jpnote import JPNote
from note.note_constants import CardTypes
from sysutils import app_thread_pool
from sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from sysutils.typed import checked_cast

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner


class CachedNote:
    def __init__(self, note: JPNote) -> None:
        self.id = note.get_id()
        self.answer = note.get_answer()
        self.question = note.get_question()

TNote = TypeVar("TNote", bound=JPNote)
TSnapshot = TypeVar("TSnapshot", bound=CachedNote)

class NoteCache(ABC, Generic[TNote, TSnapshot]):
    def __init__(self, all_notes: list[TNote], cached_note_type: type[TNote], cache_runner: CacheRunner) -> None:
        self._note_type = cached_note_type
        self._by_question: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)
        self._by_id: dict[NoteId, TNote] = {}
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}
        self._by_answer: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)
        self._pending_generated_data_updates: set[TNote] = set()

        self._deleted: set[NoteId] = set()

        self._flushing = False
        self._last_deleted_note_time = 0.0
        self._pending_add: list[Note] = list()

        for _note in all_notes:
            self._add_to_cache(_note)


        cache_runner.connect_generate_data_timer(self._update_and_persist_generated_data)
        cache_runner.connect_merge_pending_adds(self._merge_pending_added_notes)
        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_will_add(self._on_will_be_added)
        cache_runner.connect_will_flush(self._on_will_flush)

        def cache_studying_status() -> None:
            for note in all_notes:
                note.is_studying(CardTypes.reading)
                note.is_studying(CardTypes.listening)

        app_thread_pool.pool.submit(cache_studying_status)

    def all(self) -> list[TNote]:
        return list(self._by_id.values())

    def with_id(self, note_id: NoteId) -> TNote:
        return self._by_id[note_id]

    def with_question(self, question: str) -> list[TNote]:
        return list(self._by_question[question])

    def with_answer(self, answer: str) -> list[TNote]:
        return list(self._by_answer[answer])

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
            self._pending_generated_data_updates.add(note)


    def _on_will_flush(self, backend_note: Note) -> None:
        if backend_note.id and backend_note.id in self._by_id:
            assert backend_note.id not in self._deleted

            note = self._create_note(backend_note)
            self._refresh_in_cache(note)
            self._pending_generated_data_updates.add(note)

    def _on_will_be_added(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self._pending_add.append(backend_note)

    def _on_will_be_removed(self, note_ids: Sequence[NoteId]) -> None:
        self._deleted.update(note_ids)
        self._last_deleted_note_time = time.time()
        cached_notes = [self._by_id[note_id] for note_id in note_ids if note_id in self._snapshot_by_id]
        for cached in cached_notes:
            self._remove_from_cache(cached)

    def _create_note(self, backend_note: Note) -> TNote:
        return checked_cast(self._note_type, JPNote.note_from_note(backend_note))

    def _consume_pending_data_updates(self) -> set[TNote]:
        update_set = self._pending_generated_data_updates
        self._pending_generated_data_updates = set()
        return {note for note in update_set if note.get_id() not in self._deleted}

    def _update_and_persist_generated_data(self) -> None:
        for note in self._consume_pending_data_updates():
            note.update_generated_data()
            self._refresh_in_cache(note)


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
