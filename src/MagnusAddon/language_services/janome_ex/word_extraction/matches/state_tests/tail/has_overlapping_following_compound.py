from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef


class HasDisplayedOverlappingFollowingCompound(MatchStateTest, Slots):
    """Checks if this match should yield to an overlapping compound that extends beyond it.

    yield_target_matches are pre-computed (valid, non-hidden, non-yielding) in
    TextAnalysisLocation.yield_target_matches. We just check if any exist.
    """

    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match)

    @property
    @override
    def description(self) -> str: return "has_displayed_following_overlapping_compound"

    @property
    @override
    def is_cachable(self) -> bool: return True

    @override
    def _internal_match_is_in_state(self) -> bool:
        return self.end_location.compound_matches_extending_past_this_location.any(lambda it: it.is_displayed)
