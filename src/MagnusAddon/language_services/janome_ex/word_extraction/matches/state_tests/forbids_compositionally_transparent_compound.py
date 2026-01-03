from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch


class ForbidsCompositionallyTransparentCompound(MatchRequirement, Slots):
    @property
    @override
    def is_fulfilled(self) -> bool: return False

    @property
    @override
    def failure_reason(self) -> str: return "forbids::configured_to_hide_compositionally_transparent_compounds"

    @staticmethod
    def for_if(match: VocabMatch) -> ForbidsCompositionallyTransparentCompound | None:
        if (ConfigurationCache.hide_transparent_compounds()
                and match.word.analysis.for_ui
                and match.word.is_compound
                and match.vocab.matching_configuration.bool_flags.is_compositionally_transparent_compound.is_set()):
            return _instance
        return None

_instance = ForbidsCompositionallyTransparentCompound()
