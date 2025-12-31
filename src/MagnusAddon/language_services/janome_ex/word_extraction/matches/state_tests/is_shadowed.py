from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsShadowed(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match)

    @property
    @override
    def description(self) -> str: return "shadowed"

    @property
    @override
    def is_cachable(self) -> bool: return True

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.start_location.compound_matches_covering_this_location.none():
            return False
        if not self.word.is_custom_compound:
            if self.start_location.compound_matches_covering_this_location.any(IsShadowed._match_is_displayed):  # noqa: SIM103
                return True
            return False

        if self.start_location.compound_matches_covering_this_location.any(self._match_is_displayed_and_fully_covers_this_match):
            return True

        if (self.start_location.compound_matches_covering_this_location  # noqa: SIM103
                .where(IsShadowed._match_is_displayed_and_would_not_yield_to_upcoming_overlapping_compound)
                .any()):  # noqa: SIM103
            return True

        return False

    def _match_is_displayed_and_fully_covers_this_match(self, match: Match) -> bool:
        return match.word.end_location.token_index >= self.end_location.token_index and match.is_displayed

    @staticmethod
    def _match_is_displayed_and_would_not_yield_to_upcoming_overlapping_compound(match: Match) -> bool:
        return not match.would_yield_to_upcoming_overlapping_compound and match.is_displayed

    @staticmethod
    def _match_is_displayed(match: Match) -> bool:
        return match.is_displayed

    @property
    @override
    def state_description(self) -> str:
        return "shadowed_by_covering_match" if self.match_is_in_state else "forbids::shadowed"
