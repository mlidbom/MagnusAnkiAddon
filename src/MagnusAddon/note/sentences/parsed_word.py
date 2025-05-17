from __future__ import annotations

from autoslot import Slots
from note.sentences.serialization.parsed_word_serializer import ParsedWordSerializer


class ParsedWord(Slots):
    serializer:ParsedWordSerializer = ParsedWordSerializer()
    def __init__(self, word: str) -> None:
        self.word = word
