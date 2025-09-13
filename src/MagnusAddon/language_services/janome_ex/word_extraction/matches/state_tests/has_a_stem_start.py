from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services import conjugator
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class HasAStem(MatchStateTest):
    def __init__(self, match: Match) -> None:
        super().__init__(match, "a_stem")

    @property
    @override
    def match_is_in_state(self) -> bool:
        if len(self.prefix) > 0 and self.prefix[-1] in conjugator.a_stem_characters:  # noqa: SIM103
            return True

        return False
