from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services import conjugator
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasAStem(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("a_stem")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("a_stem")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.a_stem
        if requirement.is_active:
            is_in_state = len(inspector.prefix) > 0 and inspector.prefix[-1] in conjugator.a_stem_characters
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None
