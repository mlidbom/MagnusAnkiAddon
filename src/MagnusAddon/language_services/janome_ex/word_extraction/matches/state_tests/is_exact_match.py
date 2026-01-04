from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsIsExactMatch(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("exact_match")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("exact_match")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> MatchRequirement | None:
        requirement = inspector.match.requires_forbids.exact_match
        if requirement.is_active:
            is_in_state = cls._internal_is_in_state(inspector)
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None

    @staticmethod
    def _internal_is_in_state(inspector: VocabMatchInspector) -> bool:
        if not inspector.variant.is_surface:
            return False

        if inspector.variant.form in inspector.match.vocab.forms.all_set():  # noqa: SIM103
            return True
        return False
