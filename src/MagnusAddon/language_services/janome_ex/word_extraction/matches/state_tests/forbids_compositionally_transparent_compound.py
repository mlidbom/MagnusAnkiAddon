from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class ForbidsCompositionallyTransparentCompound(MatchRequirement, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        self._match: WeakRef[Match] = match
        self._is_fulfilled_cached: bool | None = None
    @property
    @override
    def is_fulfilled(self) -> bool:
        if self._is_fulfilled_cached is None:
            self._is_fulfilled_cached = not self._match().inspector.compound_locations_all_have_valid_non_compound_matches  # this condition cannot be checked until the full first stage of analysis is done, the rest has been checked below, so no need to repeat it

        return self._is_fulfilled_cached

    @property
    @override
    def failure_reason(self) -> str: return "forbids::configured_to_hide_compositionally_transparent_compounds"

    @staticmethod
    def for_if(match: WeakRef[VocabMatch]) -> ForbidsCompositionallyTransparentCompound | None:
        _match = match()
        if (ConfigurationCache.hide_transparent_compounds()
                and _match.word.analysis.for_ui
                and _match.word.is_compound
                and _match.vocab.matching_configuration.bool_flags.is_compositionally_transparent_compound.is_set()):
            return ForbidsCompositionallyTransparentCompound(match)
        return None
