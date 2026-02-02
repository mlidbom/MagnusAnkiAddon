from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsSurface(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("surface")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("surface")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.surface

        if requirement.is_required and not inspector.variant.is_surface:
            return cls._required_failure
        if requirement.is_forbidden and inspector.variant.is_surface and not inspector.base_equals_surface:
            return cls._forbidden_failure
        return None
