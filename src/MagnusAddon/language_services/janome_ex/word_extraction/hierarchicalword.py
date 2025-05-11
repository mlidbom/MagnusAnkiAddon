from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord

from typing import Optional


class HierarchicalWord:
    def __init__(self, word: ExtractedWord):
        self.word = word
        self.length = len(word.surface)
        self.shadowed_by:Optional[HierarchicalWord] = None
        self.shadowed:list[HierarchicalWord] = []
        self.start_index = self.word.character_index
        self.end_index = self.start_index + self.length - 1

    def add_shadowed(self, child:HierarchicalWord) -> None:
        self.shadowed.append(child)
        child.shadowed_by = self

    def is_shadowing(self, other: HierarchicalWord) -> bool:
        if self == other or self.shadowed_by:
            return False

        if self.start_index < other.start_index <= self.end_index:
            return True

        if self.start_index == other.start_index:
            if self.length > other.length:
                return True

            if self.word.word_length() > other.word.word_length() and other.word.word in self.word.word:
                return True

        return False

    def __repr__(self) -> str:
        return f"HierarchicalWord('{self.start_index}:{self.end_index}, {self.word.surface}:{self.word.word}: parent:{self.shadowed_by.word.word if self.shadowed_by else ''}')"
