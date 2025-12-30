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
        if self.start_location.covering_matches.none():
            return False
        if not self.word.is_custom_compound:
            return True
        if self.start_location.covering_matches.all(IsShadowed._match_would_yield_to_upcoming_overlapping_compound):  # noqa: SIM103
            return False

        return True

    @staticmethod
    def _match_would_yield_to_upcoming_overlapping_compound(match: Match) -> bool:
        return match.would_yield_to_upcoming_overlapping_compound

    @property
    @override
    def state_description(self) -> str:
        return "shadowed_by_covering_match" if self.match_is_in_state else "forbids::shadowed"
