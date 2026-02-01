from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsConfiguredIncorrect(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("configured_incorrect")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if inspector.configuration.incorrect_matches.excludes_at_index(inspector.match.exclusion_form,
                                                                       inspector.match.start_index):
            return ForbidsIsConfiguredIncorrect._failed
        return None
