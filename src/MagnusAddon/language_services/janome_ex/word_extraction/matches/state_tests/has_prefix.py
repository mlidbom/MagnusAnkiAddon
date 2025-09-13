from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class PrefixIsIn(MatchStateTest):
    def __init__(self, match: Match, allowed_prefixes: set[str]) -> None:
        super().__init__(match, f"prefix_is_in{",".join(allowed_prefixes)}")
        self.allowed_prefixes = allowed_prefixes

    @property
    @override
    def match_is_in_state(self) -> bool: return self.prefix in self.allowed_prefixes
