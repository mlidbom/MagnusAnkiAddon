from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match


class MatchStateTest:
    def __init__(self, match: Match, name: str) -> None:
        self._match: Match = match
        self.name: str = name

    @property
    def match(self) -> Match: return self._match

