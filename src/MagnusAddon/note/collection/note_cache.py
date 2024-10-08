from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar
import time

from anki.notes import Note, NoteId
from ankiutils import app
from ankiutils.audio_suppressor import audio_suppressor
from note.collection.cache_runner import CacheRunner
from note.jpnote import JPNote
from sysutils import progress_display_runner
from sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive
from sysutils.typed import checked_cast

class CachedNote:
    def __init__(self, note: JPNote):
        self.id = note.get_id()
        self.answer = note.get_answer()
        self.question = note.get_question()

TNote = TypeVar('TNote', bound=JPNote)
TSnapshot = TypeVar('TSnapshot', bound=CachedNote)

class NoteCache(ABC, Generic[TNote, TSnapshot]):
    def __init__(self, all_notes: list[TNote], cached_note_type: type[TNote], cache_runner: CacheRunner):
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

        progress_display_runner.process_with_progress(all_notes, self._add_to_cache, "initializing cache", allow_cancel=False, pause_cache_updates=False)


        cache_runner.connect_generate_data_timer(self._update_and_persist_generated_data)
        cache_runner.connect_merge_pending_adds(self._merge_pending_added_notes)
        cache_runner.connect_will_remove(self._on_will_be_removed)
        cache_runner.connect_will_add(self._on_will_be_added)
        cache_runner.connect_will_flush(self._on_will_flush)

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
        if backend_note.id:
            if backend_note.id in self._by_id:
                note = self._create_note(backend_note)
                assert backend_note.id not in self._deleted
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

    def _update_and_persist_generated_data(self) -> None:
        updates = list(note for note in self._pending_generated_data_updates if note.get_id() not in self._deleted)
        self._pending_generated_data_updates = set()
        notes_with_updated_generated_data:list[Note] = list()

        def update_generated_data(cached_note:TNote) -> None:
            backend_note = app.col().anki_collection.get_note(cached_note.get_id())  # make sure we are working with the most current data
            note = self._create_note(backend_note)
            # noinspection PyProtectedMember
            if note._internal_update_generated_data():
                notes_with_updated_generated_data.append(backend_note)
                self._refresh_in_cache(note)

        progress_display_runner.process_with_progress(updates, update_generated_data, "Updating generated data for cache updates", allow_cancel=False, delay_display=True, pause_cache_updates=False)

        if updates:
            audio_suppressor.suppress_for_seconds(.3)
            if notes_with_updated_generated_data:
                app.anki_collection().update_notes(notes_with_updated_generated_data)
                current_time = time.time()
                if current_time - self._last_deleted_note_time > 2: #We do no refreshes within two seconds of a deletion because this may crash anki
                    app.ui_utils().refresh(refresh_browser=False)


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
