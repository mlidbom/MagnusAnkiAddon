from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Generic, Self, Sequence, TypeVar

from anki import hooks
from anki.collection import Collection
from anki.notes import Note, NoteId

from note.jpnote import JPNote

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
        self._by_question: dict[str, set[TNote]] = defaultdict(set)
        self._by_id: dict[NoteId, TNote] = {}
        self._snapshot_by_id: dict[NoteId, TSnapshot] = {}
        self._by_answer: dict[str, set[TNote]] = defaultdict(set)
        self._pending_add: list[TNote] = []

        for note in all_notes:
            self._add_to_cache(note)

        self._setup_hooks()

    def all(self) -> list[TNote]: return list(self._merged_self()._by_id.values())
    def with_id(self, note_id: NoteId) -> TNote: return self._merged_self()._by_id[note_id]
    def with_question(self, question: str) -> list[TNote]: return list(self._merged_self()._by_question[question])
    def with_answer(self, answer: str) -> list[TNote]: return list(self._merged_self()._by_answer[answer])

    @abstractmethod
    def _create_snapshot(self, note: TNote) -> TSnapshot: pass
    def _inheritor_remove_from_cache(self, note: TNote, cached: TSnapshot) -> None: pass
    def _inheritor_add_to_cache(self, note: TNote) -> None: pass

    def _merge_pending(self) -> None:
        added_vocab = [v for v in self._pending_add if v.get_id()]
        self._pending_add = [v for v in self._pending_add if not v.get_id()]
        for vocab in added_vocab:
            self._add_to_cache(vocab)

    def _merged_self(self) -> Self:
        self._merge_pending()
        return self

    def _setup_hooks(self) -> None:
        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_flush.append(self._on_will_flush)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        cached_notes = [self._by_id[note_id] for note_id in note_ids if note_id in self._snapshot_by_id]
        for cached in cached_notes:
            self._remove_from_cache(cached)

    def _on_will_flush(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, self._note_type):
            if note.get_id():
                if note.get_id() in self._by_id:
                    self._remove_from_cache(note)

                self._add_to_cache(note)
            else:
                self._pending_add.append(note)

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