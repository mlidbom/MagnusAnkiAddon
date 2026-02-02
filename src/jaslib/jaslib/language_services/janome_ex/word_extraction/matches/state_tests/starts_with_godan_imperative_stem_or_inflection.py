from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsStartsWithGodanImperativeStemOrInflection(Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("godan_imperative")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("godan_imperative")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = inspector.match.requires_forbids.godan_imperative
        if requirement.is_active:
            is_in_state = inspector.word.start_location.token.is_godan_imperative_inflection or inspector.word.start_location.token.is_godan_imperative_stem
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None
