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
    start position. This match is shadowed if ANY covering word would NOT yield to it.

    Simple logic: Coverer C shadows me unless C would yield to me.
    C yields to me if: C has yield_last_token AND I'm in C's tail AND I extend beyond C.
    """

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
        from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_hidden import IsConfiguredHidden
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        my_start_idx = self.word.start_location.token_index
        my_end_idx = self.word.end_location.token_index

        for covering_word in self.word.start_location.covering_words:
            # Check if covering_word has any valid, non-hidden match that wouldn't yield to us
            for variant in covering_word.valid_variants:
                for match in variant.matches:
                    if not match.is_valid:
                        continue
                    if IsConfiguredHidden(match.weakref).match_is_in_state:
                        continue

                    # Would this match yield to us?
                    if self._would_yield_to_us(match, my_start_idx, my_end_idx):
                        continue  # It yields, doesn't shadow us

                    # This match wouldn't yield - it shadows us
                    return True

        return False

    def _would_yield_to_us(self, match: Match, my_start_idx: int, my_end_idx: int) -> bool:
        """Check if match would yield to our word."""
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

        if not isinstance(match, VocabMatch):
            return False
        if not match.requires_forbids.yield_last_token.is_required:
            return False

        # We're a valid yield target if we start in match's tail and extend beyond match
        match_start_idx = match.word.start_location.token_index
        match_end_idx = match.word.end_location.token_index

        return my_start_idx > match_start_idx and my_end_idx > match_end_idx

    @property
    @override
    def state_description(self) -> str:
        return "shadowed_by_covering_word" if self.match_is_in_state else "forbids::shadowed"
