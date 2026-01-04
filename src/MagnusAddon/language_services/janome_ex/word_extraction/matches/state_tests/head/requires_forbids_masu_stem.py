from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsMasuStem(Slots):
    _required_reason: FailedMatchRequirement = FailedMatchRequirement("forbids::masu-stem")
    _forbidden_reason: FailedMatchRequirement = FailedMatchRequirement("requires::masu-stem")

    @staticmethod
    def apply_to(inspector: VocabMatchInspector) -> MatchRequirement | None:
        if inspector.match.matching_configuration.requires_forbids.masu_stem.is_required and not inspector.has_masu_stem:
            return RequiresOrForbidsMasuStem._required_reason
        if inspector.match.matching_configuration.requires_forbids.masu_stem.is_forbidden and inspector.has_masu_stem:
            return RequiresOrForbidsMasuStem._forbidden_reason
        return None
