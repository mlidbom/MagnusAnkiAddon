from __future__ import annotations

from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class MatchStateTest:
    def __init__(self, match: Match, name: str) -> None:
        self._match: Match = match
        self.name: str = name

    @property
    def match(self) -> Match: return self._match

    @property
    def match_is_in_state(self) -> bool: raise NotImplementedError()

    @property
    def state_description(self) -> str: return self.name if self.match_is_in_state else f"not::{self.name}"

    @override
    def __repr__(self) -> str: return self.state_description
