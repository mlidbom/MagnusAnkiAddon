from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

if TYPE_CHECKING:
    from collections.abc import Callable

class WordExclusionSet:
    def __init__(self, save_callback: Callable[[],None], exclusions: list[WordExclusion]) -> None:
        self._save: Callable[[],None] = save_callback
        self._exclusions: set[WordExclusion] = set(exclusions)

    def get(self) -> set[WordExclusion]: return self._exclusions

    def words(self) -> set[str]:
        return {exclusion.word for exclusion in self._exclusions}

    def reset(self) -> None:
        self._exclusions = set()
        self._save()

    def add_str(self, vocab: str) -> None:
        self.add(WordExclusion.from_string(vocab))

    def add(self, exclusion: WordExclusion) -> None:
        self._exclusions.add(exclusion)
        self._save()

    def remove(self, exclusion: WordExclusion) -> None:
        self._exclusions.remove(exclusion)

    def remove_string(self, to_remove: str) -> None:
        for exclusion in [ex for ex in self._exclusions if ex.word == to_remove]:
            self._exclusions.remove(exclusion)
        self._save()
