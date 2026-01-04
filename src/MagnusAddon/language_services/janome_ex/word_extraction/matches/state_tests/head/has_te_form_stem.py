from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasTeFormStem(Slots):
    _te_forms: QSet[str] = QSet(("て", "って", "で"))
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("te_form_stem")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("te_form_stem")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> MatchRequirement | None:
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

        if inspector.previous_location.token.is_special_nai_negative():  # todo: review: this code means that we do not consider ない to be a te form stem, but it seems that janome does.....
            return False

        if inspector.previous_location.token.is_te_form_stem():
            return True

        if not any(te_form_start for te_form_start in RequiresOrForbidsHasTeFormStem._te_forms if inspector.parsed_form.startswith(te_form_start)):
            return False

        if inspector.previous_location.token.is_past_tense_stem():
            return True

        if inspector.previous_location.token.is_ichidan_masu_stem():  # noqa: SIM103
            return True

        return False
