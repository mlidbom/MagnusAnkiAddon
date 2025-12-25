from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class HasGodanImperativePrefix(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "te_form_stem", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.previous_location is None:
            return False

        if self.previous_location.token.is_godan_imperative_inflection:  # noqa: SIM103
            return True
        return False

