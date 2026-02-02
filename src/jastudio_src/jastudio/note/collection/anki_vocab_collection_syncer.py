from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.note_constants import NoteTypes
from jaslib.note.vocabulary.vocabnote import VocabNote
from jastudio.anki_extentions.note_bulk_loader import NoteBulkLoader
from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer

from jaslib import app

if TYPE_CHECKING:
    from anki.collection import Collection
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

class AnkiVocabCollectionSyncer(Slots):
    def __init__(self, collection: Collection, cache_manager: AnkiCollectionSyncRunner) -> None:
        all_vocab = NoteBulkLoader.load_all_notes_of_type(collection, NoteTypes.Vocab)
        self._cache: AnkiSingleCollectionSyncer[VocabNote] = AnkiSingleCollectionSyncer[VocabNote](all_vocab, VocabNote, VocabNote, app.col().vocab.cache, cache_manager)
