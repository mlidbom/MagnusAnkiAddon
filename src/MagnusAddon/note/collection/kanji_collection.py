from __future__ import annotations

from typing import Any, List

from note.collection.backend_facade import BackEndFacade
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from sysutils import ex_sequence
from sysutils.lazy import Lazy

class _CachedKanji(CachedNote):
    def __init__(self, note: KanjiNote):
        super().__init__(note)

class _Cache(NoteCache[KanjiNote, _CachedKanji]):
    def __init__(self, all_kanji: list[KanjiNote]):
        super().__init__(all_kanji)

    def all(self) -> list[KanjiNote]: return list(self._merged_self()._by_id.values())
    def with_kanji(self, kanji: str) -> list[KanjiNote]: return list(self._merged_self()._by_question[kanji])

    def _is_instance_note_type(self, instance: Any) -> bool: return isinstance(instance, KanjiNote)
    def _create_cached_note(self, note: KanjiNote) -> _CachedKanji: return _CachedKanji(note)

    def _inheritor_remove_from_cache(self, note: KanjiNote, cached:_CachedKanji) -> None: pass
    def _inheritor_add_to_cache(self, note: KanjiNote) -> None: pass

class KanjiCollection:
    def __init__(self, collection: BackEndFacade):
        self.collection = collection
        self._cache_factory = Lazy(lambda: _Cache(self._all_internal()))

    def search(self, query: str) -> list[KanjiNote]:
        return [KanjiNote(note) for note in self.collection.search_notes(query)]

    def _all_internal(self) -> List[KanjiNote]:
        notes = self.collection.fetch_notes_by_note_type(NoteTypes.Kanji)
        kanji_notes = [KanjiNote(note) for note in notes]
        return kanji_notes

    def all(self) -> list[KanjiNote]: return self._cache().all()

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def by_kanji(self, kanji_list: list[str]) -> List[KanjiNote]:
        return ex_sequence.flatten([self._cache().with_kanji(kanji) for kanji in kanji_list])

    def _cache(self) -> _Cache: return self._cache_factory.instance()
