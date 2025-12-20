from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from manually_copied_in_libraries.autoslot import Slots

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class SurfaceIsIn(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match], surfaces: set[str]) -> None:
        super().__init__(match, f"""surface_in:{",".join(surfaces)}""", cache_is_in_state=True)
        self.surfaces: set[str] = surfaces

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.word.surface_variant.form in self.surfaces:  # noqa: SIM103
            return True
        return False
