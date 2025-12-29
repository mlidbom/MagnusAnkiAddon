from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsGodanImperativeInflectionWithBase(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match)

    @property
    @override
    def description(self) -> str: return "godan_imperative_surface_with_base"

    @override
    def _internal_match_is_in_state(self) -> bool:
        if self.has_godan_imperative_part and self.word.location_count == 1 and self.variant.is_surface and self.word.base_variant is not None:  # noqa: SIM103
            return True
        return False
