from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class ForbidsConfiguredToHideCompounds(MatchRequirement, Slots):
    def __init__(self, match: Match) -> None:
        self._match: WeakRef[Match] = match.weakref
        self._is_fulfilled_cached: bool | None = None
    @property
    @override
    def is_fulfilled(self) -> bool:
        if self._is_fulfilled_cached is None:
            self._is_fulfilled_cached = not self._match().inspector.compound_locations_all_have_valid_non_compound_matches # this condition cannot be checked until the full first stage of analysis is done, the rest has been checked below, so no need to repeat it

        return self._is_fulfilled_cached

    @property
    @override
    def failure_reason(self) -> str: return "forbids::configured_to_hide_all_compounds"

    @staticmethod
    def for_if(match: Match) -> ForbidsConfiguredToHideCompounds | None:
        if (ConfigurationCache.hide_all_compounds()
                and match.inspector.word.is_compound
                and match.word.analysis.for_ui
                and not match.inspector.is_ichidan_covering_godan_potential):  # we can't tell whether it is really the potential or the ichidan in this case, so we don't hide those "compounds"
            return ForbidsConfiguredToHideCompounds(match)

        return None
