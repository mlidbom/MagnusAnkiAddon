from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsDictionaryFormPrefix(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("dictionary_form_prefix")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("dictionary_form_prefix")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.dictionary_form_prefix
        if requirement.is_active:
            is_in_state = cls._internal_is_in_state(inspector)
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None

    @classmethod
    def _internal_is_in_state(cls, inspector: VocabMatchInspector) -> bool:
        if inspector.previous_location and inspector.previous_location.token.is_dictionary_verb_inflection:  # noqa: SIM103
            return True

        return False
