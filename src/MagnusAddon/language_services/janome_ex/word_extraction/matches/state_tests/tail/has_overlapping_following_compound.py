from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from manually_copied_in_libraries.autoslot import Slots
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

    pass

class HasDisplayedOverlappingFollowingCompound(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "has_displayed_following_overlapping_compound", cache_is_in_state=False)

    @override
    def _internal_match_is_in_state(self) -> bool:
        # todo: this is a problematic reference to display_words_starting_here. That collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words_starting_here is first initialized. Ouch

        tail_location = self.end_location
        while tail_location is not self.word.start_location:
            for display_word in tail_location.display_words:
                if display_word.end_location.token_index > self.word.end_location.token_index:
                    return True

            tail_location = non_optional(tail_location.previous)()

        return False