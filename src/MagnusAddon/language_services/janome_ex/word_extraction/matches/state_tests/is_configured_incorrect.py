from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids import MatchCustomForbids
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsIsConfiguredIncorrect(MatchCustomForbids, Slots):

    _failed: MatchRequirement = FailedMatchRequirement.forbids("configured_incorrect")

    @staticmethod
    def apply_to(inspector: MatchInspector) -> MatchRequirement | None:
        if inspector.configuration.incorrect_matches.excludes_at_index(inspector.tokenized_form,
                                                                       inspector.match.start_index):
            return ForbidsIsConfiguredIncorrect._failed
        return None
