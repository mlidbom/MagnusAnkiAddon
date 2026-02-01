from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsConfiguredHidden(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("configured_hidden")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if inspector.variant.configuration.hidden_matches.excludes_at_index(inspector.match.exclusion_form,
                                                                            inspector.match.start_index):  # noqa: SIM103
            return ForbidsIsConfiguredHidden._failed
        return None
