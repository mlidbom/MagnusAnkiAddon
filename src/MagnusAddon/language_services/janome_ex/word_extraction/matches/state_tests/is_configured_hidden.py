from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids import MatchCustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class ForbidsIsConfiguredHidden(MatchCustomForbids, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, is_requirement_active=True)

    @property
    @override
    def description(self) -> str: return "configured_hidden"

    @override
    def _internal_is_in_state(self) -> bool:
        # todo: think a bit about this. Now we use the variant start index, which may differ from the match start index. Which should be used?
        if self.variant.configuration.hidden_matches.excludes_at_index(self.tokenized_form, self.variant.start_index):  # noqa: SIM103
            return True
        return False
