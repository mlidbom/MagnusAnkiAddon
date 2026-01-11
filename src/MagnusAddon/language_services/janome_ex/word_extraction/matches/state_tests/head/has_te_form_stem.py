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
        # todo get this stuff moved into the tokenizing stage...
        if inspector.previous_location is None:
            return False

        previous_token = inspector.previous_location.token

        if previous_token.is_special_nai_negative:  # todo: review: this code means that we do not consider ない to be a te form stem, but it seems that janome does.....
            return False

        if previous_token.is_te_form_stem:
            return True

        if inspector.start_location.token.surface not in RequiresOrForbidsHasTeFormStem._te_form_token_surfaces:
            return False

        if previous_token.is_past_tense_stem:
            return True

        if previous_token.is_masu_stem and not previous_token.is_godan_verb:  # noqa: SIM103
            return True

        return False
