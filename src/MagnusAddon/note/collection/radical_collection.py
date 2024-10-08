from __future__ import annotations

from typing import List

from anki.collection import Collection
from anki.notes import Note, NoteId

from note.collection.backend_facade import BackEndFacade
from note.collection.cache_runner import CacheRunner
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.radicalnote import RadicalNote
from sysutils import ex_sequence

class _RadicalSnapshot(CachedNote):
    def __init__(self, note: RadicalNote):
        super().__init__(note)

class _RadicalCache(NoteCache[RadicalNote, _RadicalSnapshot]):
    def __init__(self, all_kanji: list[RadicalNote], cache_manager: CacheRunner):
        super().__init__(all_kanji, RadicalNote, cache_manager)

    def _create_snapshot(self, note: RadicalNote) -> _RadicalSnapshot: return _RadicalSnapshot(note)

class RadicalCollection:
    def __init__(self, collection: Collection, cache_manager: CacheRunner):
        def radical_constructor(note: Note) -> RadicalNote: return RadicalNote(note)
        self.collection = BackEndFacade[RadicalNote](collection, radical_constructor, NoteTypes.Radical)
        self._cache = _RadicalCache(list(self.collection.all()), cache_manager)

    def all(self) -> List[RadicalNote]: return self._cache.all()

    def with_id(self, note_id:NoteId) -> RadicalNote:
        return self._cache.with_id(note_id)

    def with_any_answer_in(self, answers: list[str]) -> List[RadicalNote]:
        return ex_sequence.flatten([self._cache.with_answer(answer) for answer in answers])

    def with_any_question_in(self, questions: list[str]) -> List[RadicalNote]:
        return ex_sequence.flatten([self._cache.with_question(question) for question in questions])