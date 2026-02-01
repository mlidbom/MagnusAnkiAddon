from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasGodanImperativePrefix(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("godan_imperative_prefix")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("godan_imperative_prefix")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.godan_imperative_prefix
        if requirement.is_active:
            is_in_state = cls._internal_is_in_state(inspector)
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None

    @classmethod
    def _internal_is_in_state(cls, inspector: VocabMatchInspector) -> bool:
        if inspector.previous_location is None:
            return False

        if inspector.previous_location.token.is_godan_imperative_inflection:  # noqa: SIM103
            return True
        return False

