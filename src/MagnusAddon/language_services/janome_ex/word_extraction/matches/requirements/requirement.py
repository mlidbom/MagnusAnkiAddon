from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    pass

class MatchRequirement:
    def __init__(self, match: VocabMatch, name: str) -> None:
        self.match: VocabMatch = match
        self.name: str = name

    @property
    def match_is_in_state(self) -> bool: raise NotImplementedError()

