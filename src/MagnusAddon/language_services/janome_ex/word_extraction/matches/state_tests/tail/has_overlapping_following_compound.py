from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

    pass

class HasDisplayedOverlappingFollowingCompound(MatchStateTest, Slots):
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
        # This checks if there's a displayed word starting within this word's tail
        # that extends beyond this word's end position. When step 5 processes locations
        # right-to-left, display_words at forward positions are already resolved,
        # so yield decisions are made based on final display state (not stale data).

        tail_location = self.end_location
        while tail_location is not self.word.start_location:
            for display_word in tail_location.display_words:
                if display_word.end_location.token_index > self.word.end_location.token_index:
                    return True

            tail_location = non_optional(tail_location.previous)()

        return False
