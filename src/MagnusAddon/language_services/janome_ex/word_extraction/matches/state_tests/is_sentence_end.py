from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class IsSentenceEnd(MatchStateTest):
    _quote_characters = {"と", "って"}
    def __init__(self, match: Match) -> None:
        super().__init__(match, "sentence_end")

    @property
    @override
    def match_is_in_state(self) -> bool:
        if len(self.suffix) == 0:
            return True

        if self.suffix[0].isspace():
            return True

        if self.suffix in self._quote_characters:  # noqa: SIM103
            return True

        return False
