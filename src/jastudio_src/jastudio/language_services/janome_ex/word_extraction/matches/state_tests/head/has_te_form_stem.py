from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasTeFormStem(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("te_form_stem")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("te_form_stem")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.te_form_stem

        if requirement.is_required and not inspector.has_te_form_stem:
            return RequiresOrForbidsHasTeFormStem._required_failure
        if requirement.is_forbidden and inspector.has_te_form_stem:
            return RequiresOrForbidsHasTeFormStem._forbidden_failure
        return None
