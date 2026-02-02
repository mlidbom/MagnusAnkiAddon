from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.note.note_constants import NoteTypes
from jaslib.note.vocabulary.vocabnote import VocabNote
from jastudio.anki_extentions.note_ex import NoteBulkLoader
from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer

from jaslib import app

if TYPE_CHECKING:

    from anki.collection import Collection
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

class _AnkiVocabCache(AnkiSingleCollectionSyncer[VocabNote], Slots):
    def __init__(self, all_vocab: list[JPNoteData], cache_runner: AnkiCollectionSyncRunner) -> None:
        super().__init__(all_vocab, VocabNote, app.col().vocab.cache, cache_runner)


class AnkiVocabCollectionSyncer(Slots):
    def __init__(self, collection: Collection, cache_manager: AnkiCollectionSyncRunner) -> None:
        all_vocab = NoteBulkLoader.load_all_notes_of_type(collection, NoteTypes.Vocab)
        self._cache: _AnkiVocabCache = _AnkiVocabCache(all_vocab, cache_manager)

