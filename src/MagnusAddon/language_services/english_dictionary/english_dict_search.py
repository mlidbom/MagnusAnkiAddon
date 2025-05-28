from __future__ import annotations

import os

from autoslot import Slots
from sysutils.lazy import Lazy


class WordSense(Slots):
    def __init__(self, definition: str, pos: str) -> None:
        self.definition = definition
        self.pos = pos

class EnglishWord(Slots):
    def __init__(self, word: str, definition: str = "", pos: str = "") -> None:
        self.word = word
        self.lower_case_word = word.lower()
        self.senses: list[WordSense] = []

        # Add the initial sense if provided
        if definition or pos:
            self.add_sense(definition, pos)

    def add_sense(self, definition: str, pos: str) -> None:
        self.senses.append(WordSense(definition, pos))

class EnglishDictionary(Slots):
    def __init__(self) -> None:
        self.words: list[EnglishWord] = []
        self.word_map: dict[str, EnglishWord] = {}  # Map words to their EnglishWord objects

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

                    # Check if the word already exists in our dictionary
                    lower_word = word.lower()
                    if lower_word in self.word_map:
                        # Add a new sense to the existing word
                        self.word_map[lower_word].add_sense(definition, pos)
                    else:
                        # Create a new EnglishWord
                        english_word = EnglishWord(word, definition, pos)
                        self.words.append(english_word)
                        self.word_map[lower_word] = english_word

    def words_starting_with_shortest_first(self, start_of_word: str) -> list[EnglishWord]:
        search_string = start_of_word.lower()
        hits = [word for word in self.words if word.lower_case_word.startswith(search_string)]
        return sorted(hits, key=lambda word: len(word.lower_case_word))

dictionary: Lazy[EnglishDictionary] = Lazy(lambda: EnglishDictionary())