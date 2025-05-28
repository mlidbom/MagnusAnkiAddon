from __future__ import annotations

import os

from autoslot import Slots
from sysutils.lazy import Lazy


class EnglishWord(Slots):
    def __init__(self, word: str, definition: str, pos: str) -> None:
        self.word = word
        self.lower_case_word = word.lower()
        self.definition = definition
        self.pos = pos

    class Predicates:
        @staticmethod
        def starts_with(word: EnglishWord, test_for: str) -> bool:
            return word.lower_case_word.startswith(test_for)

class EnglishDictionary(Slots):
    def __init__(self) -> None:
        self.words: list[EnglishWord] = []

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(current_dir, "data", "english_words.csv")

        with open(data_file_path, encoding="utf-8") as file:
            next(file)
            for line in file:
                parts = line.strip().split(",", 2)

                if parts and parts[0]:
                    word = parts[0]
                    pos = parts[1] if len(parts) > 1 else ""
                    definition = parts[2] if len(parts) > 2 else ""
                    self.words.append(EnglishWord(word, definition, pos))

    def words_starting_with_shortest_first(self, start_of_word: str) -> list[EnglishWord]:
        search_string = start_of_word.lower()
        hits = [word for word in self.words if word.lower_case_word.startswith(search_string)]
        return sorted(hits, key=lambda word: len(word.lower_case_word))


dictionary = Lazy(lambda: EnglishDictionary())