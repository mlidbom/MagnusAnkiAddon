from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.vocab_match_state_test import VocabMatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    pass

class AnotherMatchOwnsTheForm(VocabMatchStateTest):
    def __init__(self, match: VocabMatch) -> None:
        super().__init__(match, "another_match_owns_the_form")

    @property
    @override
    def match_is_in_state(self) -> bool: return self.match.is_secondary_match