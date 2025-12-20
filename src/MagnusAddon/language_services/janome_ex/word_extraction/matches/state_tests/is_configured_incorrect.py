from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from autoslot import Slots  # type: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsConfiguredIncorrect(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "configured_incorrect", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        return self.configuration.incorrect_matches.excludes_at_index(self.tokenized_form,
                                                                      self.match.start_index)
