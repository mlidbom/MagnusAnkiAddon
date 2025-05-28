from __future__ import annotations

from autoslot import Slots


class EnglishWord(Slots):
    def __init__(self, word: str, definition: str, pos: str) -> None:
        self.word = word
        self.definition = definition
        self.pos = pos

class EnglishDictionary(Slots):
    def __init__(self) -> None:
        self.words: dict[str, EnglishWord] = {}

        with open("data/english_words.csv", encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = line.strip().split(",", 2)

                if parts and parts[0]:
                    word = parts[0]
                    pos = parts[1] if len(parts) > 1 else ""
                    definition = parts[2] if len(parts) > 2 else ""
                    self.words[word] = EnglishWord(word, definition, pos)