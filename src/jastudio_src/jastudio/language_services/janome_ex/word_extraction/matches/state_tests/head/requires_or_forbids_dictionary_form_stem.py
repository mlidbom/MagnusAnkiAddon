from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsDictionaryFormStem(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("dictionary_form_stem")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("dictionary_form_stem")
    _forbidden_by_default_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("dictionary_form_stem_forbidden_by_default")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.dictionary_form_stem

        is_in_state = cls._internal_is_in_state(inspector)
        if is_in_state:
            if requirement.is_required:
                return None
            if requirement.is_forbidden:
                return cls._forbidden_failure
            return cls._forbidden_by_default_failure

        if requirement.is_required:
            return cls._required_failure

        return None

    @classmethod
    def _internal_is_in_state(cls, inspector: VocabMatchInspector) -> bool:
        if inspector.start_location_is_dictionary_verb_inflection:  # noqa: SIM103
            return True

        return False
