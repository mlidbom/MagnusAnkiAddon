from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_custom_forbids import VocabMatchCustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

    pass

class ForbidsCompositionallyTransparentCompound(VocabMatchCustomForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector, is_requirement_active=True)

    @property
    @override
    def description(self) -> str: return "configured_to_hide_compositionally_transparent_compounds"

    @override
    def _internal_is_in_state(self) -> bool:
        if self.inspector.match.vocab.matching_configuration.bool_flags.is_compositionally_transparent_compound.is_set():
            return True
        return False

    @staticmethod
    def for_if(inspector: VocabMatchInspector, is_enabled: bool) -> ForbidsCompositionallyTransparentCompound | None:
        return ForbidsCompositionallyTransparentCompound(inspector) if is_enabled else None
