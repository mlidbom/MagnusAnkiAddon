from __future__ import annotations

from collections import defaultdict
from typing import List, Self, Sequence

from anki import hooks
from anki.collection import Collection
from anki.notes import Note, NoteId

from note.collection.backend_facade import BackEndFacade
from note.jpnote import JPNote
from note.note_constants import NoteFields, NoteTypes
from note.radicalnote import RadicalNote
from sysutils import ex_sequence
from sysutils.lazy import Lazy

class _CachedRadical:
    def __init__(self, note: RadicalNote):
        self.id = note.get_id()
        self.question = note.get_question()
        self.answer = note.get_answer()

class _Cache:
    def __init__(self, all_radical: list[RadicalNote]):
        self._by_question: dict[str, set[RadicalNote]] = defaultdict(set)
        self._by_answer: dict[str, set[RadicalNote]] = defaultdict(set)
        self._by_id: dict[NoteId, RadicalNote] = {}
        self._cached_by_id: dict[NoteId, _CachedRadical] = {}
        self._pending_add: list[RadicalNote] = []

        for radical in all_radical:
            self._add_to_cache(radical)

        self._setup_hooks()

    def all(self) -> list[RadicalNote]: return list(self._merged_self()._by_id.values())
    def with_radical(self, radical: str) -> list[RadicalNote]: return list(self._merged_self()._by_question[radical])
    def with_answer(self, answer: str) -> list[RadicalNote]: return list(self._merged_self()._by_answer[answer])

    def _merge_pending(self) -> None:
        added_radical = [v for v in self._pending_add if v.get_id()]
        self._pending_add = [v for v in self._pending_add if not v.get_id()]
        for radical in added_radical:
            self._add_to_cache(radical)

    def _merged_self(self) -> Self:
        self._merge_pending()
        return self

    def _setup_hooks(self) -> None:
        hooks.notes_will_be_deleted.append(self._on_will_be_removed)
        hooks.note_will_flush.append(self._on_will_flush)

    def _on_will_be_removed(self, _: Collection, note_ids: Sequence[NoteId]) -> None:
        cached_notes = [self._by_id[note_id] for note_id in note_ids if note_id in self._cached_by_id]
        for cached in cached_notes:
            self._remove_from_cache(cached)

    # noinspection DuplicatedCode
    def _on_will_flush(self, backend_note: Note) -> None:
        note = JPNote.note_from_note(backend_note)
        if isinstance(note, RadicalNote):
            if note.get_id():
                if note.get_id() in self._by_id:
                    self._remove_from_cache(note)

                self._add_to_cache(note)
            else:
                self._pending_add.append(note)

    def _remove_from_cache(self, note: RadicalNote) -> None:
        assert note.get_id()
        cached = self._cached_by_id.pop(note.get_id())
        self._by_id.pop(note.get_id())
        self._by_question[cached.question].discard(note)
        self._by_answer[cached.answer].discard(note)

    def _add_to_cache(self, note: RadicalNote) -> None:
        assert note.get_id()
        self._by_id[note.get_id()] = note
        self._cached_by_id[note.get_id()] = _CachedRadical(note)
        self._by_question[note.get_question()].add(note)
        self._by_answer[note.get_answer()].add(note)

class RadicalCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache_factory = Lazy(lambda: _Cache(self._all_internal()))

    def all(self) -> List[RadicalNote]: return self._cache().all()

    def by_answer(self, field_values: list[str]) -> List[RadicalNote]:
        return ex_sequence.flatten([self._cache().with_answer(answer) for answer in field_values])

    def _all_internal(self) -> List[RadicalNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Radical)
        radical_notes = [RadicalNote(note) for note in notes]
        return radical_notes

    def _cache(self) -> _Cache: return self._cache_factory.instance()