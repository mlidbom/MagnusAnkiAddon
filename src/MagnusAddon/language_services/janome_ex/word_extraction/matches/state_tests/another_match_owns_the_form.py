from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.vocab_match_state_test import VocabMatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

    pass

class AnotherMatchOwnsTheForm(VocabMatchStateTest, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match, "another_match_owns_the_form", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.vocab.forms.is_owned_form(self.tokenized_form):
            return False

        if any(other_match for other_match in self.variant.vocab_matches  # noqa: SIM103
               if other_match != self.match
                  and other_match.vocab.forms.is_owned_form(self.tokenized_form)
                  and other_match.is_valid):
            return True
        return False
