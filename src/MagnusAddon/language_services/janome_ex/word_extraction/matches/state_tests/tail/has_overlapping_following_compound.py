from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids_no_cache import CustomForbidsNoCache
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

    pass

class ForbidsHasDisplayedOverlappingFollowingCompound(CustomForbidsNoCache, Slots):
    def __init__(self, match: WeakRef[VocabMatch], is_requirement_active: bool = True) -> None:
        super().__init__(match, is_requirement_active)

    @property
    @override
    def description(self) -> str: return "has_displayed_following_overlapping_compound"

    @override
    def _internal_is_in_state(self) -> bool:
        # todo: this is a problematic reference to display_words. That collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words is first initialized. Ouch

        tail_location = self.end_location
        while tail_location is not self.word.start_location:
            for display_word in tail_location.display_words:
                if display_word.end_location.token_index > self.word.end_location.token_index:
                    return True

            tail_location = non_optional(tail_location.previous)()

        return False
