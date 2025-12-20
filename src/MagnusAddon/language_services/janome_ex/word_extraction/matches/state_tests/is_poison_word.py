from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.vocab_match_state_test import VocabMatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef
    pass

class IsPoisonWord(VocabMatchStateTest, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match, "poison_word", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.rules.bool_flags.is_poison_word.is_set():  # noqa: SIM103
            return True
        return False
