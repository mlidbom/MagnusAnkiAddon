from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.note_constants import NoteTypes
from jaslib.note.sentences.sentencenote import SentenceNote
from jastudio.anki_extentions.note_ex import NoteBulkLoader
from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer

from jaslib import app

if TYPE_CHECKING:
    from anki.collection import Collection
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

class _AnkiSentenceCache(AnkiSingleCollectionSyncer[SentenceNote], Slots):
    def __init__(self, all_kanji: list[JPNoteData], cache_runner: AnkiCollectionSyncRunner) -> None:
        super().__init__(all_kanji, SentenceNote, SentenceNote, app.col().sentences.cache, cache_runner)


class AnkiSentenceCollectionSyncer(Slots):
    def __init__(self, collection: Collection, cache_manager: AnkiCollectionSyncRunner) -> None:
        all_notes = NoteBulkLoader.load_all_notes_of_type(collection, NoteTypes.Sentence)
        self._cache: _AnkiSentenceCache = _AnkiSentenceCache(all_notes, cache_manager)
