from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction import analysis_constants
from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsIsSentenceStart(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("sentence_start")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("sentence_start")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.matching_configuration.requires_forbids.sentence_start
        if requirement.is_active:
            is_in_state = len(inspector.prefix) == 0 or inspector.prefix[-1] in analysis_constants.sentence_start_characters
            if requirement.is_required and not is_in_state:
                return RequiresOrForbidsIsSentenceStart._required_failure
            if requirement.is_forbidden and is_in_state:
                return RequiresOrForbidsIsSentenceStart._forbidden_failure
        return None
