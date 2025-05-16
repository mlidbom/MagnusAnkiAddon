from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from collections.abc import Callable


class WordExclusionSet:
    def __init__(self, save_callback: Callable[[],None], exclusions: list[WordExclusion]) -> None:
        self._save: Callable[[],None] = save_callback
        self._exclusions: set[WordExclusion] = set(exclusions)
        self._instance_tracker = ObjectInstanceTracker(WordExclusionSet)

    def get(self) -> set[WordExclusion]: return self._exclusions

    def words(self) -> set[str]:
        return {exclusion.word for exclusion in self._exclusions}

    def reset(self) -> None:
        self._exclusions = set()
        self._save()

    def add_global(self, vocab: str) -> None:
        self.add(WordExclusion.global_(vocab))

    def add(self, exclusion: WordExclusion) -> None:
        self._exclusions.add(exclusion)
        self._save()

    def remove(self, exclusion: WordExclusion) -> None:
        self._exclusions.remove(exclusion)

    def remove_string(self, to_remove: str) -> None:
        for exclusion in [ex for ex in self._exclusions if ex.word == to_remove]:
            self._exclusions.remove(exclusion)
        self._save()

    def excludes_at_index(self, word:str, index:int) -> bool:
        return any(exclusion for exclusion in self._exclusions if exclusion.excludes_form_at_index(word, index))

    def __repr__(self) -> str: return ", ".join(exclusion.__repr__() for exclusion in self._exclusions)
