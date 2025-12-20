from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction import analysis_constants
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsSentenceEnd(MatchStateTest, Slots):

    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "sentence_end", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if len(self.suffix) == 0:
            return True

        if self.suffix[0].isspace():
            return True

        if self.suffix in analysis_constants.sentence_end_characters:  # noqa: SIM103
            return True

        return False
