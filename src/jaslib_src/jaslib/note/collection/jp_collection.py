from __future__ import annotations

from autoslot import Slots

from jaslib import mylog
from jaslib.note.collection.kanji_collection import KanjiCollection
from jaslib.note.collection.sentence_collection import SentenceCollection
from jaslib.note.collection.vocab_collection import VocabCollection
from jaslib.sysutils.weak_ref import WeakRefable


class JPCollection(WeakRefable, Slots):
    def __init__(self) -> None:
        self._is_initialized: bool = False
        self._initialization_started: bool = False

        mylog.info("JPCollection.__init__")

        self._vocab: VocabCollection = VocabCollection()
        self._kanji: KanjiCollection = KanjiCollection()
        self._sentences: SentenceCollection = SentenceCollection()

    # noinspection PyUnusedFunction
    @property
    def is_initialized(self) -> bool: return self._is_initialized
    @property
    def vocab(self) -> VocabCollection: return self._vocab
    @property
    def kanji(self) -> KanjiCollection: return self._kanji
    @property
    def sentences(self) -> SentenceCollection: return self._sentences
