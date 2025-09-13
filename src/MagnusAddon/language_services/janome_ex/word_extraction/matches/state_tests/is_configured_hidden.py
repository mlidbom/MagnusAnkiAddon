from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class IsConfiguredHidden(MatchStateTest):
    def __init__(self, match: Match) -> None:
        super().__init__(match, "is_shadowed")

    @property
    @override
    def match_is_in_state(self) -> bool:
        #todo: think a bit about this. Now we use the variant start index, which may differ from the match start index. Which should be used?
        if self.variant.configuration.hidden_matches.excludes_at_index(self.tokenized_form, self.variant.start_index):  # noqa: SIM103
            return True
        return False
