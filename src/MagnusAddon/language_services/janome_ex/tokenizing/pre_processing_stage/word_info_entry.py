from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from typed_linq_collections.collections.q_set import QSet


class WordInfoEntry(Slots):
    def __init__(self, word: str, pos: QSet[str]) -> None:
        self.word: str = word
        self.parts_of_speech: QSet[str] = pos.select(lambda x: x.lower()).to_set()

    @property
    def is_ichidan(self) -> bool: return "ichidan verb" in self.parts_of_speech

    @property
    def is_godan(self) -> bool: return "godan verb" in self.parts_of_speech

    @property
    def is_intransitive(self) -> bool: return "intransitive" in self.parts_of_speech
