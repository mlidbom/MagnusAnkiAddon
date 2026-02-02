from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from typed_linq_collections.collections.q_default_dict import QDefaultDict

if TYPE_CHECKING:
    from anki.collection import Collection
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.cache_runner import CacheRunner

from jaslib.note.kanjinote import KanjiNote
from jaslib.note.note_constants import NoteTypes
from jastudio.note.collection.anki_note_cache import AnkiCachedNote, AnkiNoteCache
from jastudio.note.collection.backend_facade import BackEndFacade
from typed_linq_collections.collections.q_list import QList


@final
class _AnkiKanjiSnapshot(AnkiCachedNote, Slots):
    def __init__(self, note: KanjiNote) -> None:
        super().__init__(note)

class _AnkiKanjiCache(AnkiNoteCache[KanjiNote, _AnkiKanjiSnapshot], Slots):
    def __init__(self, all_kanji: list[KanjiNote], cache_runner: CacheRunner) -> None:
        # Since notes with a given Id are guaranteed to only exist once in the cache, we can use lists within the dictionary to cut memory usage a ton compared to using sets
        self._by_radical: QDefaultDict[str, QList[KanjiNote]] = QDefaultDict(QList[KanjiNote])
        self.by_reading: QDefaultDict[str, QList[KanjiNote]] = QDefaultDict(QList[KanjiNote])
        super().__init__(all_kanji, KanjiNote, cache_runner)

    @override
    def _create_snapshot(self, note: KanjiNote) -> _AnkiKanjiSnapshot: return _AnkiKanjiSnapshot(note)

class AnkiKanjiCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def kanji_constructor_call_while_populating_kanji_collection(data: JPNoteData) -> KanjiNote: return KanjiNote(data)
        self._backend_facade: BackEndFacade[KanjiNote] = BackEndFacade[KanjiNote](collection, kanji_constructor_call_while_populating_kanji_collection, NoteTypes.Kanji)
        all_kanji = self._backend_facade.all()
        self._cache: _AnkiKanjiCache = _AnkiKanjiCache(all_kanji, cache_manager)