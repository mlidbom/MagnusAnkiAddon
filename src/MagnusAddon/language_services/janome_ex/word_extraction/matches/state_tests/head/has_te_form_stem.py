from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasTeFormStem(Slots):
    _te_form_token_surfaces: set[str] = {"て", "って", "で", "てる"}
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("te_form_stem")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("te_form_stem")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.te_form_stem
        if requirement.is_active:
            is_in_state = RequiresOrForbidsHasTeFormStem._internal_is_in_state(inspector)
            if requirement.is_required and not is_in_state:
                return RequiresOrForbidsHasTeFormStem._required_failure
            if requirement.is_forbidden and is_in_state:
                return RequiresOrForbidsHasTeFormStem._forbidden_failure
        return None

    @classmethod
    def _internal_is_in_state(cls, inspector: VocabMatchInspector) -> bool:
        previous_location = inspector.previous_location
        return previous_location is not None and previous_location.token.is_te_form_stem
