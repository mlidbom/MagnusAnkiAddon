from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import AutoSlots
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsGodanPotentialSurface(MatchStateTest, AutoSlots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "godan_potential", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.word.start_location.token.is_potential_godan and self.word.location_count == 1 and self.variant.is_surface:  # noqa: SIM103
            return True
        return False
