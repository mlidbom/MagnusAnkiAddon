from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class SuffixIsIn(MatchStateTest):
    def __init__(self, match: Match, suffixes: set[str], true_if_no_suffixes: bool) -> None:
        super().__init__(match, f"""suffix_is_in:{",".join(suffixes)}""")
        self.true_if_no_suffixes: bool = true_if_no_suffixes
        self.suffixes: set[str] = suffixes

    @property
    @override
    def match_is_in_state(self) -> bool:
        if self.true_if_no_suffixes and not any(self.suffixes):
            return True

        if any(suffix for suffix in self.suffixes if self.suffix.startswith(suffix)):  # noqa: SIM103
            return True

        return False
