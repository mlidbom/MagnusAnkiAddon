from __future__ import annotations

from autoslot import Slots
from note.vocabulary.pos_set_interner import POSSetManager


class WordInfoEntry(Slots):
    def __init__(self, word: str, pos: frozenset[str]) -> None:
        self.word: str = word
        self.parts_of_speech: frozenset[str] = pos

    @property
    def is_ichidan(self) -> bool: return POSSetManager.ICHIDAN_VERB in self.parts_of_speech

    @property
    def is_godan(self) -> bool: return POSSetManager.GODAN_VERB in self.parts_of_speech

    @property
    def is_intransitive(self) -> bool: return POSSetManager.INTRANSITIVE in self.parts_of_speech
