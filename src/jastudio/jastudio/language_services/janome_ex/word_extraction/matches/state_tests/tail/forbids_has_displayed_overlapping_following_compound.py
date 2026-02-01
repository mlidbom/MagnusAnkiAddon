from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction.matches.requirements.custom_forbids_no_cache import CustomForbidsNoCache
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

    pass

class ForbidsHasDisplayedOverlappingFollowingCompound(CustomForbidsNoCache, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> ForbidsHasDisplayedOverlappingFollowingCompound | None:
        return ForbidsHasDisplayedOverlappingFollowingCompound(inspector) if inspector.requires_forbids.yield_last_token.is_required and not inspector.match.is_highlighted else None

    @property
    @override
    def description(self) -> str: return "has_displayed_following_overlapping_compound"

    @override
    def _internal_is_in_state(self) -> bool:
        # todo: this is a problematic reference to display_words. That collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words is first initialized. Ouch

        end_location = self.inspector.end_location
        tail_location = end_location
        # The dictionary verb inflection is a special case that is shown as a separate token after the word in wich it is part, so it does not by itself cover/shadow anything
        # thus, we skip such tokens as possible locations for following compounds to overlap, since that words starting with that token are shown after this compound anyway, and are not hidden by this compound.
        # this logic is mirrored in is_shadowed logic
        if end_location.token.is_dictionary_verb_inflection:
            if end_location.previous is None:
                return False
            tail_location = end_location.previous()

        while tail_location is not self.inspector.word.start_location:
            for display_word in tail_location.display_words:
                if display_word.end_location.token_index > end_location.token_index:
                    return True

            tail_location = non_optional(tail_location.previous)()

        return False
