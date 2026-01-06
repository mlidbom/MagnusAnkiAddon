from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsSurfaceIsInvalidSurfaces(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("split_token_surface")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> MatchRequirement | None:
        if inspector.variant.is_surface and inspector.word.end_location.token.surface_is_invalid:
            return cls._failed
        return None
