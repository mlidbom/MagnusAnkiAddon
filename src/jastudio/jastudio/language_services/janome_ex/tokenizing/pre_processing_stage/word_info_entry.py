from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from note.vocabulary.pos import POS

if TYPE_CHECKING:
    from jastudio.language_services.jamdict_ex.dict_lookup_result import DictLookupResult
    from note.vocabulary.vocabnote import VocabNote


class WordInfoEntry(Slots):
    def __init__(self, word: str, pos: frozenset[str]) -> None:
        self.word: str = word
        self.parts_of_speech: frozenset[str] = pos

    @property
    def is_ichidan(self) -> bool: return POS.ICHIDAN_VERB in self.parts_of_speech

    @property
    def is_godan(self) -> bool: return POS.GODAN_VERB in self.parts_of_speech

    @property
    def is_intransitive(self) -> bool: return POS.INTRANSITIVE in self.parts_of_speech

    @property
    def answer(self) -> str: raise NotImplementedError()


class VocabWordInfoEntry(WordInfoEntry, Slots):
    def __init__(self, word: str, vocab: VocabNote) -> None:
        self.vocab: VocabNote = vocab
        super().__init__(word, vocab.parts_of_speech.get())

    @property
    @override
    def answer(self) -> str: return self.vocab.get_answer()


class DictWordInfoEntry(WordInfoEntry, Slots):
    def __init__(self, word: str, dict_result: DictLookupResult) -> None:
        self.dict_result: DictLookupResult = dict_result
        super().__init__(word, dict_result.parts_of_speech())

    @property
    @override
    def answer(self) -> str: return self.dict_result.format_answer()
