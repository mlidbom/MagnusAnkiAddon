from __future__ import annotations

from typing import TYPE_CHECKING, final

from autoslot import Slots
from jastudio.anki_extentions.note_ex import NoteBulkLoader

if TYPE_CHECKING:
    from anki.collection import Collection
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

from jaslib.note.kanjinote import KanjiNote
from jaslib.note.note_constants import NoteTypes
from jastudio.note.collection.anki_single_collection_syncer import AnkiCachedNote, AnkiSingleCollectionSyncer

from jaslib import app


@final
class _AnkiKanjiSnapshot(AnkiCachedNote, Slots):
    def __init__(self, note: KanjiNote) -> None:
        super().__init__(note)

class _AnkiKanjiCache(AnkiSingleCollectionSyncer[KanjiNote, _AnkiKanjiSnapshot], Slots):
    def __init__(self, all_kanji: list[JPNoteData], cache_runner: AnkiCollectionSyncRunner) -> None:
        super().__init__(all_kanji, KanjiNote, app.col().kanji.cache, cache_runner)

class AnkiKanjiCollectionSyncer(Slots):
    def __init__(self, collection: Collection, cache_manager: AnkiCollectionSyncRunner) -> None:
        all_kanji = NoteBulkLoader.load_all_notes_of_type(collection, NoteTypes.Kanji)
        self._cache: _AnkiKanjiCache = _AnkiKanjiCache(all_kanji, cache_manager)