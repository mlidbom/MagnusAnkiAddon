from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsIsConfiguredHidden(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("configured_hidden")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> MatchRequirement | None:
        if inspector.variant.configuration.hidden_matches.excludes_at_index(inspector.tokenized_form, inspector.variant.start_index):  # noqa: SIM103
            return ForbidsIsConfiguredHidden._failed
        return None
