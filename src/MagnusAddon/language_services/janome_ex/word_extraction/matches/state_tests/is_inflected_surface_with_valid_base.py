from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids import MatchCustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class ForbidsIsInflectedSurfaceWithValidBase(MatchCustomForbids, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, is_requirement_active=True)

    @property
    @override
    def description(self) -> str: return "inflected_surface_with_valid_base"

    @override
    def _internal_is_in_state(self) -> bool:
        return self.variant.is_surface and self.word.is_inflected_word and self.word.has_base_variant_with_valid_match
