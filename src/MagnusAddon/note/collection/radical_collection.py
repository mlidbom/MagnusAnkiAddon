from __future__ import annotations

from collections import defaultdict
from typing import List

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.radicalnote import RadicalNote
from sysutils import ex_sequence

class _RadicalSnapshot(CachedNote):
    def __init__(self, note: RadicalNote):
        super().__init__(note)

class _RadicalCache(NoteCache[RadicalNote, _RadicalSnapshot]):
    def __init__(self, all_kanji: list[RadicalNote]):
        super().__init__(all_kanji, RadicalNote)

    def _create_snapshot(self, note: RadicalNote) -> _RadicalSnapshot: return _RadicalSnapshot(note)

class RadicalCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache = _RadicalCache([RadicalNote(note) for note in (self.collection.fetch_notes_by_note_type(NoteTypes.Radical))])

    def all(self) -> List[RadicalNote]: return self._cache.all()

    def with_any_answer_in(self, field_values: list[str]) -> List[RadicalNote]:
        return ex_sequence.flatten([self._cache.with_answer(answer) for answer in field_values])