from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids_no_cache import CustomForbidsNoCache
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

    pass

class ForbidsHasDisplayedOverlappingFollowingCompound(CustomForbidsNoCache, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @staticmethod
    def apply_to(inspector: VocabMatchInspector, is_active: bool) -> ForbidsHasDisplayedOverlappingFollowingCompound | None:
        return ForbidsHasDisplayedOverlappingFollowingCompound(inspector) if is_active else None

    @property
    @override
    def description(self) -> str: return "has_displayed_following_overlapping_compound"

    @override
    def _internal_is_in_state(self) -> bool:
        # todo: this is a problematic reference to display_words. That collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words is first initialized. Ouch

        tail_location = self.inspector.end_location
        while tail_location is not self.inspector.word.start_location:
            for display_word in tail_location.display_words:
                if display_word.end_location.token_index > self.inspector.word.end_location.token_index:
                    return True

            tail_location = non_optional(tail_location.previous)()

        return False
