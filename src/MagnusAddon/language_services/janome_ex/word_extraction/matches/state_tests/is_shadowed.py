from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef


class IsShadowed(MatchStateTest, Slots):
    """Checks if this match is shadowed by a covering word.

    A covering word is one that starts BEFORE this match and extends OVER this match's
    start position. This match is shadowed if ANY covering word would still be displayed
    even knowing this match exists.

    The key insight: instead of checking "Is coverer displayed?" (circular), we ask
    "Would coverer be displayed if I was displayed?" The coverer answers by checking
    if it would yield to us - this is answerable without knowing final display states.
    """

    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match)

    @property
    @override
    def description(self) -> str: return "shadowed"

    @property
    @override
    def is_cachable(self) -> bool: return True  # Now cacheable - no circular dependencies!

    def _internal_match_is_in_state(self) -> bool:
        # Check each covering word (words starting earlier that extend over our start)
        for covering_word in self.word.start_location.covering_words:
            # Skip if covering word is shorter or same length - it can't shadow us
            if covering_word.location_count <= self.word.location_count:
                continue

            # Ask: "Would this covering word be displayed if I (this match) was displayed?"
            # If yes, it shadows us. If no (because it would yield to us), it doesn't.
            if self._would_covering_word_be_displayed_given_this_match(covering_word):
                return True

        return False

    def _would_covering_word_be_displayed_given_this_match(self, covering_word: CandidateWord) -> bool:
        """Check if covering_word would be displayed given that this match exists and is valid.

        The covering_word would NOT be displayed if it would yield to this match (or to
        something beyond this match). It WOULD be displayed if it doesn't yield.

        Also checks that the covering_word's matches are not hidden (via exclusions).
        """
        from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_hidden import IsConfiguredHidden

        # Check if any of covering_word's matches would be displayed
        for variant in covering_word.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                # Check if this match is hidden via exclusions
                if IsConfiguredHidden(match.weakref).match_is_in_state:
                    continue  # Hidden matches don't shadow

                # Would this match yield to our match (self.match)?
                if self._would_match_yield_to(match, self.word):
                    continue  # It would yield, so it wouldn't shadow us

                # This match wouldn't yield to us and isn't hidden - it would be displayed and shadow us
                return True

        return False

    def _would_match_yield_to(self, match: Match, target_word: CandidateWord) -> bool:
        """Check if match would yield to target_word (or something beyond it)."""
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        # Only VocabMatch can have yield_last_token requirement
        if not isinstance(match, VocabMatch):
            return False

        if not match.requires_forbids.yield_last_token.is_required:
            return False

        # Check if target_word is a valid yield target for match
        # (starts in match's tail and extends beyond match)
        match_start_idx = match.word.start_location.token_index
        match_end_idx = match.word.end_location.token_index
        target_start_idx = target_word.start_location.token_index
        target_end_idx = target_word.end_location.token_index

        if target_start_idx > match_start_idx and target_end_idx > match_end_idx:
            # target_word is a valid yield target - match would yield to it
            return True

        # Check if match would yield to something beyond target_word
        for candidate in match.word.end_location.yield_target_candidates:
            candidate_start_idx = candidate.start_location.token_index
            if candidate_start_idx > match_start_idx and candidate.end_location.token_index > match_end_idx:
                # This is a valid yield target - but would IT be displayed?
                # Recursively check if candidate would be displayed
                if self._would_yield_target_be_displayed(candidate, match.word):
                    return True

        return False

    def _would_yield_target_be_displayed(self, candidate: CandidateWord, yielder: CandidateWord) -> bool:
        """Check if candidate would be displayed (not shadowed and not yielding)."""
        for variant in candidate.valid_variants:
            for match in variant.matches:
                if not match.is_valid:
                    continue

                # Would this match yield to something further?
                if self._would_match_yield_further(match):
                    continue

                # This match wouldn't yield - candidate would be displayed
                return True

        return False

    def _would_match_yield_further(self, match: Match) -> bool:
        """Check if match would yield to any valid compound beyond it."""
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        if not isinstance(match, VocabMatch):
            return False

        if not match.requires_forbids.yield_last_token.is_required:
            return False

        match_start_idx = match.word.start_location.token_index
        match_end_idx = match.word.end_location.token_index

        for candidate in match.word.end_location.yield_target_candidates:
            candidate_start_idx = candidate.start_location.token_index
            if candidate_start_idx > match_start_idx and candidate.end_location.token_index > match_end_idx:
                if self._would_yield_target_be_displayed(candidate, match.word):
                    return True

        return False

    @property
    @override
    def state_description(self) -> str:
        return f"shadowed_by_covering_word" if self.match_is_in_state else "forbids::shadowed"
