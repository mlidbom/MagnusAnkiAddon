from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, override

from jaslib.sysutils.abstract_method_called_error import AbstractMethodCalledError

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNoteId
    from jaslib.note.kanjinote import KanjiNote
    from jaslib.note.sentences.sentencenote import SentenceNote
    from jaslib.note.vocabulary.vocabnote import VocabNote

class IBackendNoteCreator(metaclass=ABCMeta):
    __slots__: tuple[str, ...] = ()
    @abstractmethod
    def create_kanji(self, note: KanjiNote) -> JPNoteId: raise AbstractMethodCalledError()
    @abstractmethod
    def create_vocab(self, note: VocabNote) -> JPNoteId: raise AbstractMethodCalledError()
    @abstractmethod
    def create_sentence(self, note: SentenceNote) -> JPNoteId: raise AbstractMethodCalledError()

class TestingBackendNoteCreator(IBackendNoteCreator):
    __slots__: tuple[str, ...] = ("_current_id",)
    def __init__(self) -> None:
        self._current_id: JPNoteId = 0

    def _get_next_id(self) -> JPNoteId:
        self._current_id += 1
        return self._current_id

    @override
    def create_kanji(self, note: KanjiNote) -> JPNoteId: return self._get_next_id()
    @override
    def create_vocab(self, note: VocabNote) -> JPNoteId: return self._get_next_id()
    @override
    def create_sentence(self, note: SentenceNote) -> JPNoteId: return self._get_next_id()
