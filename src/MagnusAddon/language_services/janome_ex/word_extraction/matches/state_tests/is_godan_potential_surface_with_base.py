from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsGodanPotentialInflectionWithBase(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "godan_potential_surface", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.has_godan_potential_part and self.word.location_count == 1 and self.variant.is_surface and self.word.base_variant is not None:  # noqa: SIM103
            return True
        return False
