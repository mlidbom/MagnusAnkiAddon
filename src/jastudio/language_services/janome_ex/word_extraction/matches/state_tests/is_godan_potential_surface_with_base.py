from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsGodanPotentialInflectionWithBase(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("godan_potential_surface")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if inspector.has_godan_potential_start and inspector.word.location_count == 1 and inspector.variant.is_surface and inspector.word.base_variant is not None:  # noqa: SIM103:
            return ForbidsIsGodanPotentialInflectionWithBase._failed
        return None
