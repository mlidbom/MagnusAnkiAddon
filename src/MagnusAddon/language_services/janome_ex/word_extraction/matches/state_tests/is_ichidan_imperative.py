from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection(CustomRequiresOrForbids, Slots):
    _required_failure: FailedMatchRequirement = FailedMatchRequirement.required("ichidan_imperative")
    _forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids("ichidan_imperative")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> MatchRequirement | None:
        requirement = inspector.match.requires_forbids.ichidan_imperative
        if requirement.is_active:
            is_in_state = inspector.word.start_location.token.is_ichidan_imperative_stem or inspector.word.start_location.token.is_ichidan_imperative_inflection
            if requirement.is_required and not is_in_state:
                return cls._required_failure
            if requirement.is_forbidden and is_in_state:
                return cls._forbidden_failure
        return None