from __future__ import annotations

from typing import List

from anki.collection import Collection
from anki.notes import Note

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from sysutils import ex_sequence

class _KanjiSnapshot(CachedNote):
    def __init__(self, note: KanjiNote):
        super().__init__(note)

class _KanjiCache(NoteCache[KanjiNote, _KanjiSnapshot]):
    def __init__(self, all_kanji: list[KanjiNote]):
        super().__init__(all_kanji, KanjiNote)

    def _create_snapshot(self, note: KanjiNote) -> _KanjiSnapshot: return _KanjiSnapshot(note)

class KanjiCollection:
    def __init__(self, collection: Collection):
        def kanji_constructor(note: Note) -> KanjiNote: return KanjiNote(note)
        self.collection = BackEndFacade[KanjiNote](collection, kanji_constructor, NoteTypes.Kanji)
        self._cache = _KanjiCache(list(self.collection.all()))

    def search(self, query: str) -> list[KanjiNote]:
        return list(self.collection.search(query))

    def all(self) -> list[KanjiNote]: return self._cache.all()

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def with_any_kanji(self, kanji_list: list[str]) -> List[KanjiNote]:
        return ex_sequence.flatten([self._cache.with_question(kanji) for kanji in kanji_list])
