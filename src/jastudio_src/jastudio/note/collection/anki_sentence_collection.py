from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jaslib.note.note_constants import NoteTypes
from jaslib.note.sentences.sentencenote import SentenceNote
from jastudio.note.collection.anki_note_cache import AnkiCachedNote, AnkiNoteCache
from jastudio.note.collection.backend_facade import BackEndFacade

if TYPE_CHECKING:
    from anki.collection import Collection
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.cache_runner import CacheRunner

class _AnkiSentenceSnapshot(AnkiCachedNote, Slots):
    def __init__(self, note: SentenceNote) -> None:
        super().__init__(note)

class _AnkiSentenceCache(AnkiNoteCache[SentenceNote, _AnkiSentenceSnapshot], Slots):
    def __init__(self, all_kanji: list[SentenceNote], cache_runner: CacheRunner) -> None:
        super().__init__(all_kanji, SentenceNote, cache_runner)

    @override
    def _create_snapshot(self, note: SentenceNote) -> _AnkiSentenceSnapshot: return _AnkiSentenceSnapshot(note)

class AnkiSentenceCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def sentence_constructor_call_while_populating_sentence_collection(data: JPNoteData) -> SentenceNote: return SentenceNote(data)
        self._backend_facade: BackEndFacade[SentenceNote] = BackEndFacade[SentenceNote](collection, sentence_constructor_call_while_populating_sentence_collection, NoteTypes.Sentence)
        all_sentences = list(self._backend_facade.all())
        self._cache: _AnkiSentenceCache = _AnkiSentenceCache(all_sentences, cache_manager)
