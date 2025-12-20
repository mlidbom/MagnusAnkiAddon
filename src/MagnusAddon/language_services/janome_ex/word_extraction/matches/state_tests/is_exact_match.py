from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.vocab_match_state_test import VocabMatchStateTest
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

    pass

class IsExactMatch(VocabMatchStateTest, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match, "exact_match", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if not self.variant.is_surface:
            return False

        if self.variant.form in self.vocab.forms.all_set():  # noqa: SIM103
            return True
        return False
