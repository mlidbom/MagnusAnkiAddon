from __future__ import annotations

from abc import ABC, abstractmethod
from time import sleep
from typing import Any, Generic, Sequence, TypeVar
import time

from anki import hooks
from anki.collection import Collection
from anki.notes import Note, NoteId
from aqt import mw, qconnect
from PyQt6.QtCore import QTimer

from ankiutils import app
from ankiutils.audio_suppressor import audio_suppressor
from note.jpnote import JPNote
from sysutils import progress_display_runner
from sysutils.collections.default_dict_case_insensitive import DefaultDictCaseInsensitive

class CachedNote:
    def __init__(self, note: JPNote):
        self.id = note.get_id()
        self.answer = note.get_answer()
        self.question = note.get_question()

TNote = TypeVar('TNote', bound=JPNote)
TSnapshot = TypeVar('TSnapshot', bound=CachedNote)

class NoteCache(ABC, Generic[TNote, TSnapshot]):
    def __init__(self, all_notes: list[TNote], cached_note_type: type[TNote]):
        self._note_type = cached_note_type
        self._by_question: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)
        self._by_id: dict[NoteId, TNote] = {}
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}
        self._by_answer: DefaultDictCaseInsensitive[set[TNote]] = DefaultDictCaseInsensitive(set)
        self._updates: set[TNote] = set()

        self._deleted: set[NoteId] = set()

        self._flushing = False
        self._last_deleted_note_time = 0.0
        self._updates_paused = False
        self._pending_add: list[Note] = list()

        progress_display_runner.process_with_progress(all_notes, self._add_to_cache, "initializing cache", allow_cancel=False, pause_cache_updates=False)

        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_be_added.append(self._on_will_be_added)
        hooks.note_will_flush.append(self._on_will_flush)

        self._timer = QTimer(mw)
        qconnect(self._timer.timeout, self.flush_updates)
        self._timer.start(100)  # 1000 milliseconds = 1 second


    def destruct(self) -> None:
        self.pause_cache_updates()

        while self._flushing:
            sleep(.01)

        self._timer.stop()
        self._timer.disconnect()

        hooks.notes_will_be_deleted.remove(self._on_will_be_removed)
        hooks.note_will_flush.remove(self._on_will_flush)
        hooks.note_will_be_added.remove(self._on_will_be_added)

    def all(self) -> list[TNote]:
        return list(self._by_id.values())

    def with_id(self, note_id: NoteId) -> TNote:
        return self._by_id[note_id]

    def with_question(self, question: str) -> list[TNote]:
        return list(self._by_question[question])

    def with_answer(self, answer: str) -> list[TNote]:
        return list(self._by_answer[answer])

    def pause_cache_updates(self) -> None:
        self._updates_paused = True

    def resume_cache_updates(self) -> None:
        self._updates_paused = False

    @abstractmethod
    def _create_snapshot(self, note: TNote) -> TSnapshot: pass
    def _inheritor_remove_from_cache(self, note: TNote, cached: TSnapshot) -> None: pass
    def _inheritor_add_to_cache(self, note: TNote) -> None: pass

    def _merge_pending(self) -> None:
        completely_added_list = [pending for pending in self._pending_add if pending.id]
        for backend_note in completely_added_list:
            self._pending_add.remove(backend_note)
            note = JPNote.note_from_note(backend_note)
            assert isinstance(note, self._note_type)
            self._updates.add(note)


    def _on_will_flush(self, backend_note: Note) -> None:
        if backend_note.id:
            if backend_note.id in self._by_id:
                self._updates.add(self._by_id[backend_note.id])

    def _on_will_be_added(self, _ignore1:Any, backend_note: Note, _ignore_2:Any) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            self._pending_add.append(backend_note)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        self._deleted.update(note_ids)
        self._last_deleted_note_time = time.time()
        cached_notes = [self._by_id[note_id] for note_id in note_ids if note_id in self._snapshot_by_id]
        for cached in cached_notes:
            self._remove_from_cache(cached)

    def flush_updates(self) -> None:
        if self._updates_paused: return

        self._merge_pending()
        updates = list(note for note in self._updates if note.get_id() not in self._deleted)
        self._updates = set()
        updated_notes:list[Note] = list()

        def update_note(old_note:TNote) -> None:
            backend_note = app.col().anki_collection.get_note(old_note.get_id())  # our instance is surely outdated, get a new one.
            note = JPNote.note_from_note(backend_note)
            assert isinstance(note, self._note_type)
            # noinspection PyProtectedMember
            if note._internal_update_generated_data():
                updated_notes.append(backend_note)
            if note.get_id() in self._by_id:
                self._remove_from_cache(note)

            self._add_to_cache(note)

        progress_display_runner.process_with_progress(updates, update_note, "Updating cache", allow_cancel=False, delay_display=True , pause_cache_updates=False)


        if updates:
            audio_suppressor.suppress_for_seconds(.3)
            if updated_notes:
                app.anki_collection().update_notes(updated_notes)
                current_time = time.time()
                if current_time - self._last_deleted_note_time > 2: #We do no refreshes within two seconds of a deletion because this may crash anki
                    app.ui_utils().refresh(refresh_browser=False)

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
