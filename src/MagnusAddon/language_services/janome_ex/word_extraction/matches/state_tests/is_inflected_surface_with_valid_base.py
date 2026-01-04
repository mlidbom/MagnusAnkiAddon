from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("inflected_surface_with_valid_base")

    @staticmethod
    def apply_to(inspector: MatchInspector) -> MatchRequirement | None:
        if (inspector.variant.is_surface
                and inspector.word.has_base_variant_with_valid_match
                and (inspector.word.is_inflected_word or (inspector.prefix.endswith("を") and inspector.is_end_of_statement))):
            return ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb._failed
        return None
