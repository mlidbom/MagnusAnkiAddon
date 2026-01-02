from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids import MatchCustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsGodanImperativeInflectionWithBase(MatchCustomForbids, Slots):
    def __init__(self, inspector: MatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def description(self) -> str: return "godan_imperative_surface_with_base"

    @override
    def _internal_is_in_state(self) -> bool:
        if self.inspector.has_godan_imperative_part and self.inspector.word.location_count == 1 and self.inspector.variant.is_surface and self.inspector.word.base_variant is not None:  # noqa: SIM103
            return True
        return False
