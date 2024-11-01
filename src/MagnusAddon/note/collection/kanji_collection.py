from __future__ import annotations

from collections import defaultdict
from typing import List, Optional, TYPE_CHECKING

from note.collection.cache_runner import CacheRunner

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection

from anki.collection import Collection
from anki.notes import Note, NoteId
from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from sysutils import ex_list, ex_sequence

class _KanjiSnapshot(CachedNote):
    def __init__(self, note: KanjiNote):
        super().__init__(note)
        self.radicals = set(note.get_radicals())

class _KanjiCache(NoteCache[KanjiNote, _KanjiSnapshot]):
    def __init__(self, all_kanji: list[KanjiNote], cache_runner: CacheRunner):
        self._by_radical: dict[str, set[KanjiNote]] = defaultdict(set)
        super().__init__(all_kanji, KanjiNote, cache_runner)

    def _create_snapshot(self, note: KanjiNote) -> _KanjiSnapshot: return _KanjiSnapshot(note)

    def _inheritor_remove_from_cache(self, note: KanjiNote, cached:_KanjiSnapshot) -> None:
        for form in cached.radicals: self._by_radical[form].remove(note)

    def _inheritor_add_to_cache(self, note: KanjiNote) -> None:
        for form in note.get_radicals(): self._by_radical[form].add(note)

    def with_radical(self, radical: str) -> list[KanjiNote]: return list(self._by_radical[radical])

class KanjiCollection:
    def __init__(self, collection: Collection, jp_collection: JPCollection, cache_manager: CacheRunner):
        def kanji_constructor(note: Note) -> KanjiNote: return KanjiNote(note)
        self.jp_collection = jp_collection
        self.collection = BackEndFacade[KanjiNote](collection, kanji_constructor, NoteTypes.Kanji)
        self._cache = _KanjiCache(list(self.collection.all()), cache_manager)

    def search(self, query: str) -> list[KanjiNote]:
        return list(self.collection.search(query))

    def all(self) -> list[KanjiNote]: return self._cache.all()

    def with_id(self, note_id:NoteId) -> KanjiNote:
        return self._cache.with_id(note_id)

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def with_any_kanji_in(self, kanji_list: list[str]) -> List[KanjiNote]:
        return ex_sequence.flatten([self._cache.with_question(kanji) for kanji in kanji_list])

    def with_kanji(self, kanji: str) -> Optional[KanjiNote]:
        found = self._cache.with_question(kanji)
        return found[0] if found else None

    def with_radical(self, radical:str) -> list[KanjiNote]: return self._cache.with_radical(radical)

    def with_question(self, kanji: str) -> KanjiNote:
        return ex_list.single(self._cache.with_question(kanji))
