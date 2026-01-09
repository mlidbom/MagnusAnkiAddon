from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
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
            previous_location = inspector.previous_location
            new_is_in_state = previous_location and previous_location.token.is_irrealis and previous_location.token.is_godan_verb

            if requirement.is_required and not new_is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and new_is_in_state:
                return cls._forbidden_failure
        return None
