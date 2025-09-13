from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.vocab_match_state_test import VocabMatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch

    pass

class YieldToFollowingOverlappingCompound(VocabMatchStateTest):
    def __init__(self, match: VocabMatch) -> None:
        super().__init__(match, "yield_to_following_overlapping_compound")

    @property
    @override
    def match_is_in_state(self) -> bool:
        if not self.rules.requires_forbids.yield_last_token.is_required:
            return False

        # todo: this is a problematic reference to display_words_starting_here. Thot collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words_starting_here is first initialized. Ouch
        if not any(self.end_location.display_words):
            return False

        if self.end_location.display_words[0].is_custom_compound:  # noqa: SIM103
            return True

        return False