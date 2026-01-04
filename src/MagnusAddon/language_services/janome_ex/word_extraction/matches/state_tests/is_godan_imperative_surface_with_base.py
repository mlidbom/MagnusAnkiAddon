from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsIsGodanImperativeInflectionWithBase(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("godan_imperative_surface_with_base")

    @staticmethod
    def apply_to(inspector: MatchInspector) -> MatchRequirement | None:
        if inspector.has_godan_imperative_part and inspector.word.location_count == 1 and inspector.variant.is_surface and inspector.word.base_variant is not None:  # noqa: SIM103
            return ForbidsIsGodanImperativeInflectionWithBase._failed
        return None