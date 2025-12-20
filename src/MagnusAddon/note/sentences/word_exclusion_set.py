from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

if TYPE_CHECKING:
    from collections.abc import Callable

class WordExclusionSet(Slots):
    def __init__(self, save_callback: Callable[[], None], exclusions: list[WordExclusion]) -> None:
        self._save: Callable[[], None] = save_callback
        self._exclusions: set[WordExclusion] = set(exclusions)
        self._excluded_words: set[str] = self._extract_words()

    def get(self) -> set[WordExclusion]: return self._exclusions

    def _extract_words(self) -> set[str]:
        return {exclusion.word for exclusion in self._exclusions}

    def words(self) -> set[str]:
        return self._excluded_words

    def reset(self) -> None:
        self._exclusions = set()
        self._excluded_words = set()
        self._save()

    def add_global(self, vocab: str) -> None:
        self.add(WordExclusion.global_(vocab))

    def add(self, exclusion: WordExclusion) -> None:
        self._exclusions.add(exclusion)
        self._excluded_words = self._extract_words()
        self._save()

    def remove(self, exclusion: WordExclusion) -> None:
        self._exclusions.remove(exclusion)
        self._excluded_words = self._extract_words()
        self._save()

    def remove_string(self, to_remove: str) -> None:
        for exclusion in [ex for ex in self._exclusions if ex.word == to_remove]:
            self._exclusions.remove(exclusion)
        self._excluded_words = self._extract_words()
        self._save()

    def excludes_at_index(self, word: str, index: int) -> bool:
        return any(exclusion for exclusion in self._exclusions if exclusion.excludes_form_at_index(word, index))

    @override
    def __repr__(self) -> str: return ", ".join(exclusion.__repr__() for exclusion in self._exclusions)
