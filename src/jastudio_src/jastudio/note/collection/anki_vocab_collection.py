from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jaslib.note.note_constants import NoteTypes
from jaslib.note.vocabulary.vocabnote import VocabNote
from jastudio.note.collection.anki_note_cache import AnkiCachedNote, AnkiNoteCache
from jastudio.note.collection.backend_facade import BackEndFacade

if TYPE_CHECKING:

    from anki.collection import Collection
    from jaslib.note.jpnote_data import JPNoteData
    from jastudio.note.collection.cache_runner import CacheRunner

class _AnkiVocabSnapshot(AnkiCachedNote, Slots):
    def __init__(self, note: VocabNote) -> None:
        super().__init__(note)

class _AnkiVocabCache(AnkiNoteCache[VocabNote, _AnkiVocabSnapshot], Slots):
    def __init__(self, all_vocab: list[VocabNote], cache_runner: CacheRunner) -> None:
        super().__init__(all_vocab, VocabNote, cache_runner)


    @override
    def _create_snapshot(self, note: VocabNote) -> _AnkiVocabSnapshot: return _AnkiVocabSnapshot(note)


class AnkiVocabCollection(Slots):
    def __init__(self, collection: Collection, cache_manager: CacheRunner) -> None:
        def vocab_constructor_call_while_populating_vocab_collection(data: JPNoteData) -> VocabNote: return VocabNote(data)
        self._backend_facade: BackEndFacade[VocabNote] = BackEndFacade[VocabNote](collection, vocab_constructor_call_while_populating_vocab_collection, NoteTypes.Vocab)
        all_vocab = self._backend_facade.all()
        self._cache: _AnkiVocabCache = _AnkiVocabCache(all_vocab, cache_manager)

