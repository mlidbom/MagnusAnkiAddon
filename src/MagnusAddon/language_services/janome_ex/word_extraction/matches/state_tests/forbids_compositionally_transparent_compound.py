from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsCompositionallyTransparentCompound(MatchRequirement, Slots):
    @property
    def is_fulfilled(self) -> bool: return False

    @property
    def failure_reason(self) -> str: return "forbids::configured_to_hide_compositionally_transparent_compounds"

    @staticmethod
    def for_if(inspector: VocabMatchInspector, is_enabled: bool) -> ForbidsCompositionallyTransparentCompound | None:
        return ForbidsCompositionallyTransparentCompound() if is_enabled else None
