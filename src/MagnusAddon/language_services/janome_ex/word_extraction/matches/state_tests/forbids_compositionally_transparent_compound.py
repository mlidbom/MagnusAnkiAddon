from __future__ import annotations

from typing import override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement  # pyright: ignore[reportMissingTypeStubs]


class ForbidsCompositionallyTransparentCompound(MatchRequirement, Slots):
    @property
    @override
    def is_fulfilled(self) -> bool: return False

    @property
    @override
    def failure_reason(self) -> str: return "forbids::configured_to_hide_compositionally_transparent_compounds"

    @staticmethod
    def for_if(is_enabled: bool) -> ForbidsCompositionallyTransparentCompound | None:
        return ForbidsCompositionallyTransparentCompound() if is_enabled else None
