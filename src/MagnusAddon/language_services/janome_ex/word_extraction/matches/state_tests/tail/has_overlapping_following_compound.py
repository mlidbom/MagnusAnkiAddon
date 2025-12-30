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

    This implements a "negotiation" between matches: instead of asking "Is the overlapping
    compound displayed?" (which creates circular dependencies), we ask "Would the overlapping
    compound be displayed if this match yielded to it?"

    The covering compounds are pre-computed during analysis step 2 and stored in
    TextAnalysisLocation.covering_compounds_extending_beyond for efficient lookup.
    """

    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match)

    @property
    @override
    def description(self) -> str: return "has_displayed_following_overlapping_compound"

    @property
    @override
    def is_cachable(self) -> bool: return False

    @property
    @override
    def match_is_in_state(self) -> bool:
        # Get pre-computed yield target candidates at our end location.
        # Filter for those starting in our tail (after our start position).
        my_start_idx = self.word.start_location.token_index
        my_end_idx = self.word.end_location.token_index

        for compound in self.end_location.yield_target_candidates:
            compound_start_idx = compound.start_location.token_index
            # Must start in our tail (after our start) and extend beyond our end
            if compound_start_idx > my_start_idx and compound.end_location.token_index > my_end_idx:
                if self._would_compound_be_displayed_if_we_yield(compound):
                    return True

        return False

    def _would_compound_be_displayed_if_we_yield(self, compound: CandidateWord) -> bool:
        """Check if compound would be displayed assuming we (the current match) yield.

        If we yield, we won't be displayed, so we won't shadow the compound.
        The compound is displayed if it has valid matches that don't yield to something else.
        """
        for variant in compound.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                # Check if this match would yield to something further
                if self._match_would_yield_to_displayed_compound(match):
                    continue  # This match yields, check next

                # This match doesn't yield and is valid - compound would be displayed
                return True

        return False

    def _match_would_yield_to_displayed_compound(self, match: Match) -> bool:
        """Check if match would yield to another compound that would be displayed."""
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        # Only VocabMatch can have yield_last_token requirement
        if not isinstance(match, VocabMatch):
            return False

        # Check if this match has yield_last_token active
        if not match.requires_forbids.yield_last_token.is_required:
            return False

        # Use pre-computed yield target candidates for this match's end location
        match_start_idx = match.word.start_location.token_index
        match_end_idx = match.word.end_location.token_index

        for candidate in match.word.end_location.yield_target_candidates:
            candidate_start_idx = candidate.start_location.token_index
            # Must start in match's tail and extend beyond match's end
            if candidate_start_idx > match_start_idx and candidate.end_location.token_index > match_end_idx:
                if self._would_compound_be_displayed_given_chain(candidate):
                    return True  # Match yields to this displayed compound

        return False

    def _would_compound_be_displayed_given_chain(self, compound: CandidateWord) -> bool:
        """Recursively check if compound would be displayed in the yield chain."""
        for variant in compound.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                if self._match_would_yield_to_displayed_compound(match):
                    continue

                return True

        return False
