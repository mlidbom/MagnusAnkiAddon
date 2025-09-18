from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import AutoSlots
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

    pass

class HasDisplayedOverlappingFollowingCompound(MatchStateTest, AutoSlots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "has_displayed_following_overlapping_compound", cache_is_in_state=False)

    @override
    def _internal_match_is_in_state(self) -> bool:
        # todo: this is a problematic reference to display_words_starting_here. Thot collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words_starting_here is first initialized. Ouch
        if not any(self.end_location.display_words):
            return False

        if self.end_location.display_words[0].is_custom_compound:  # noqa: SIM103
            return True

        return False