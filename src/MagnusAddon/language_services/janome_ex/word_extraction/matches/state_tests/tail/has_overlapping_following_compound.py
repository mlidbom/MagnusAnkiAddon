from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef


class HasDisplayedOverlappingFollowingCompound(MatchStateTest, Slots):
    """Checks if this match should yield to an overlapping compound that extends beyond it.

    Yield to a compound B if: B starts in our tail, extends beyond us, AND B wouldn't itself yield.
    This handles chains: if A→B→C, then A doesn't yield because B yields, so B won't be displayed.
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
        my_start_idx = self.word.start_location.token_index
        my_end_idx = self.word.end_location.token_index

        for compound in self.end_location.yield_target_candidates:
            compound_start_idx = compound.start_location.token_index
            if compound_start_idx > my_start_idx and compound.end_location.token_index > my_end_idx:
                # Would this compound be displayed? Only if it has a match that doesn't yield
                if self._compound_has_non_yielding_match(compound):
                    return True

        return False

    def _compound_has_non_yielding_match(self, compound: CandidateWord) -> bool:
        """Check if compound has any valid match that wouldn't yield to something beyond it."""
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        for variant in compound.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                # Does this match yield?
                if isinstance(match, VocabMatch) and match.requires_forbids.yield_last_token.is_required:
                    # Check if there's something to yield to
                    if self._has_yield_target(match):
                        continue  # This match yields, check next

                # This match doesn't yield - compound would be displayed
                return True

        return False

    def _has_yield_target(self, match: Match) -> bool:
        """Check if match has a valid yield target (recursively handles chains)."""
        match_start_idx = match.word.start_location.token_index
        match_end_idx = match.word.end_location.token_index

        for candidate in match.word.end_location.yield_target_candidates:
            candidate_start_idx = candidate.start_location.token_index
            if candidate_start_idx > match_start_idx and candidate.end_location.token_index > match_end_idx:
                # Would this candidate be displayed?
                if self._compound_has_non_yielding_match(candidate):
                    return True

        return False
