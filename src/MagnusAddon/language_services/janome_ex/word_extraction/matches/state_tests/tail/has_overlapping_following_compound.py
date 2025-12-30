from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

    pass

class HasDisplayedOverlappingFollowingCompound(MatchStateTest, Slots):
    """Checks if this match should yield to an overlapping compound that extends beyond it.

    This implements a "negotiation" between matches: instead of asking "Is the overlapping
    compound displayed?" (which creates circular dependencies), we ask "Would the overlapping
    compound be displayed if this match yielded to it?"

    The key insight is that if this match (A) yields to compound B:
    - A would not be displayed (it yielded)
    - So A would not shadow B
    - B's display status only depends on B's own validity and yield decisions

    This breaks the circular dependency because the question becomes "Would B be displayed
    in a world where A yielded?" rather than "Is B currently displayed?"
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
        # Find overlapping compounds in our tail that extend beyond us
        overlapping_compounds = self._get_valid_overlapping_compounds_extending_beyond()

        # Check if any of them would be displayed if we yielded to them
        return any(self._would_compound_be_displayed_if_we_yield(compound) for compound in overlapping_compounds)

    def _get_valid_overlapping_compounds_extending_beyond(self) -> list[CandidateWord]:
        """Find all valid candidate words starting in our tail that extend beyond our end."""
        result: list[CandidateWord] = []

        tail_location = self.end_location
        while tail_location is not self.word.start_location:
            for candidate_word in tail_location.valid_words:
                if candidate_word.end_location.token_index > self.word.end_location.token_index:
                    result.append(candidate_word)

            tail_location = non_optional(tail_location.previous)()

        return result

    def _would_compound_be_displayed_if_we_yield(self, compound: CandidateWord) -> bool:
        """Check if compound would be displayed assuming we (the current match) yield.

        If we yield, we won't be displayed, so we won't shadow the compound.
        The compound is displayed if:
        1. It has valid matches that pass validity requirements
        2. It's not shadowed by something else (other than us)
        3. It doesn't yield to yet another compound, OR that compound wouldn't be displayed
        """
        # Check if compound has any matches that would be valid for display
        # (ignoring shadowing since we're computing hypothetically)
        for variant in compound.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                # Check if this match would yield to something further
                if self._match_would_yield_to_displayed_compound(match, excluding_yielder=self.word):
                    continue  # This match yields, check next

                # This match doesn't yield and is valid - compound would be displayed
                return True

        return False

    def _match_would_yield_to_displayed_compound(self, match: Match, excluding_yielder: CandidateWord) -> bool:
        """Check if match would yield to another compound that would be displayed.

        This recursively follows the yield chain. The chain terminates because:
        - Each step moves to a compound ending further right
        - Eventually we reach a compound with nothing beyond it to yield to
        """
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        # Only VocabMatch can have yield_last_token requirement
        if not isinstance(match, VocabMatch):
            return False

        # Check if this match has yield_last_token active
        if not match.requires_forbids.yield_last_token.is_required:
            return False

        # Find what this match could yield to
        for candidate in self._get_overlapping_compounds_for(match.word):
            if candidate.end_location.token_index <= match.word.end_location.token_index:
                continue  # Must extend beyond

            if candidate is excluding_yielder:
                continue  # Don't consider the original yielder

            # Check if this candidate would be displayed
            if self._would_compound_be_displayed_given_chain(candidate, excluding_yielder):
                return True  # Match yields to this displayed compound

        return False

    def _get_overlapping_compounds_for(self, word: CandidateWord) -> list[CandidateWord]:
        """Find compounds starting in word's tail."""
        result: list[CandidateWord] = []

        tail_location = word.end_location
        while tail_location is not word.start_location:
            for candidate in tail_location.valid_words:
                result.append(candidate)
            tail_location = non_optional(tail_location.previous)()

        return result

    def _would_compound_be_displayed_given_chain(self, compound: CandidateWord, excluding_yielder: CandidateWord) -> bool:
        """Recursively check if compound would be displayed in the yield chain."""
        for variant in compound.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                if self._match_would_yield_to_displayed_compound(match, excluding_yielder):
                    continue

                return True

        return False
