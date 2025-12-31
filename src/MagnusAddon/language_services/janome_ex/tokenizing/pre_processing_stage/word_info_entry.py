from __future__ import annotations

from autoslot import Slots


class WordInfoEntry(Slots):
    def __init__(self, word: str, pos: frozenset[str]) -> None:
        self.word: str = word
        self.parts_of_speech: frozenset[str] = pos

    @property
    def is_ichidan(self) -> bool: return "ichidan verb" in self.parts_of_speech

    @property
    def is_godan(self) -> bool: return "godan verb" in self.parts_of_speech

    @property
    def is_intransitive(self) -> bool: return "intransitive" in self.parts_of_speech
