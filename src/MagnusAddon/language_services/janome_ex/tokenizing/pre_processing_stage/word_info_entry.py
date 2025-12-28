from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from typed_linq_collections.collections.q_frozen_set import QFrozenSet
    pass


class WordInfoEntry(Slots):
    def __init__(self, word: str, pos: QFrozenSet[str]) -> None:
        self.word: str = word
        self.parts_of_speech: QFrozenSet[str] = pos

    @property
    def is_ichidan(self) -> bool: return "ichidan verb" in self.parts_of_speech

    @property
    def is_godan(self) -> bool: return "godan verb" in self.parts_of_speech

    @property
    def is_intransitive(self) -> bool: return "intransitive" in self.parts_of_speech
