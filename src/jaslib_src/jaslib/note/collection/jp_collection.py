from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaspythonutils.sysutils.weak_ref import WeakRefable

from jaslib import mylog
from jaslib.note.collection.kanji_collection import KanjiCollection
from jaslib.note.collection.sentence_collection import SentenceCollection
from jaslib.note.collection.vocab_collection import VocabCollection

if TYPE_CHECKING:
    from jaslib.note.backend_note_creator import IBackendNoteCreator


class JPCollection(WeakRefable, Slots):
    def __init__(self, backend_note_creator: IBackendNoteCreator) -> None:
        self._is_initialized: bool = False
        self._initialization_started: bool = False

        mylog.info("JPCollection.__init__")

        self._vocab: VocabCollection = VocabCollection(backend_note_creator)
        self._kanji: KanjiCollection = KanjiCollection(backend_note_creator)
        self._sentences: SentenceCollection = SentenceCollection(backend_note_creator)

    # noinspection PyUnusedFunction
    @property
    def is_initialized(self) -> bool: return self._is_initialized
    @property
    def vocab(self) -> VocabCollection: return self._vocab
    @property
    def kanji(self) -> KanjiCollection: return self._kanji
    @property
    def sentences(self) -> SentenceCollection: return self._sentences
