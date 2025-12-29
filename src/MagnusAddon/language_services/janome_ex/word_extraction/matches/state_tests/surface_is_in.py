from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_set import QSet

class SurfaceIsIn(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match], surfaces: QSet[str]) -> None:
        super().__init__(match)
        self.surfaces: QSet[str] = surfaces

    @property
    @override
    def description(self) -> str: return f"""surface_in:{",".join(self.surfaces)}"""

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.word.surface_variant.form in self.surfaces:  # noqa: SIM103
            return True
        return False
