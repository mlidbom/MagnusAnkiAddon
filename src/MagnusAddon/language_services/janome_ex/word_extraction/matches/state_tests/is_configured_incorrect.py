from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids import MatchCustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsConfiguredIncorrect(MatchCustomForbids, Slots):
    def __init__(self, inspector: MatchInspector) -> None:
        super().__init__(inspector, is_requirement_active=True)

    @property
    @override
    def description(self) -> str: return "configured_incorrect"

    @override
    def _internal_is_in_state(self) -> bool:
        return self.inspector.configuration.incorrect_matches.excludes_at_index(self.inspector.tokenized_form,
                                                                      self.inspector.match.start_index)
