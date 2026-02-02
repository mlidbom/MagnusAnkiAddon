from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jastudio.anki_extentions.note_ex import NoteBulkLoader

if TYPE_CHECKING:
    from anki.collection import Collection
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

from jaslib.note.kanjinote import KanjiNote
from jaslib.note.note_constants import NoteTypes
from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer

from jaslib import app


class AnkiKanjiCollectionSyncer(Slots):
    def __init__(self, collection: Collection, cache_manager: AnkiCollectionSyncRunner) -> None:
        all_vocab = NoteBulkLoader.load_all_notes_of_type(collection, NoteTypes.Vocab)
        self._cache: AnkiSingleCollectionSyncer[KanjiNote] = AnkiSingleCollectionSyncer[KanjiNote](all_vocab, KanjiNote, KanjiNote, app.col().kanji.cache, cache_manager)
