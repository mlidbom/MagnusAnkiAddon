from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsIsSentenceEnd(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("sentence_end")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("sentence_end")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.sentence_end
        if requirement.is_active:
            is_in_state = inspector.is_end_of_statement
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None