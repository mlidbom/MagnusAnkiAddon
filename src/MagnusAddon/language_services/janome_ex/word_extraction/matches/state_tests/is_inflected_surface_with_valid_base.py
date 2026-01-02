from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids import MatchCustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb(MatchCustomForbids, Slots):
    def __init__(self, inspector: MatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def description(self) -> str: return "inflected_surface_with_valid_base"

    @override
    def _internal_is_in_state(self) -> bool:
        # nouns are not inflected
        if self.inspector.variant.is_surface and self.inspector.word.has_base_variant_with_valid_match:
            if self.inspector.word.is_inflected_word:
                return True
            elif self.inspector.prefix.endswith("を") and self.inspector.is_end_of_statement:
                return True
            return False

        return False
