from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.note_constants import NoteTypes
from note.radicalnote import RadicalNote
from sysutils import ex_sequence

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId
    from note.collection.cache_runner import CacheRunner


class _RadicalSnapshot(CachedNote, Slots):
    def __init__(self, note: RadicalNote) -> None:
        super().__init__(note)

class _RadicalCache(NoteCache[RadicalNote, _RadicalSnapshot], Slots):
    def __init__(self, all_kanji: list[RadicalNote], cache_runner: CacheRunner) -> None:
        super().__init__(all_kanji, RadicalNote, cache_runner)

    def _create_snapshot(self, note: RadicalNote) -> _RadicalSnapshot: return _RadicalSnapshot(note)

class RadicalCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def radical_constructor(note: Note) -> RadicalNote: return RadicalNote(note)
        self.collection = BackEndFacade[RadicalNote](collection, radical_constructor, NoteTypes.Radical)
        self._cache = _RadicalCache(list(self.collection.all()), cache_manager)

    def all(self) -> list[RadicalNote]: return self._cache.all()

    def with_id(self, note_id:NoteId) -> RadicalNote:
        return self._cache.with_id(note_id)

    def with_any_answer_in(self, answers: list[str]) -> list[RadicalNote]:
        return ex_sequence.flatten([self._cache.with_answer(answer) for answer in answers])