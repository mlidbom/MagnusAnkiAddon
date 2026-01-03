from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class ForbidsConfiguredToHideCompounds(MatchRequirement, Slots):
    @property
    @override
    def is_fulfilled(self) -> bool: return False

    @property
    @override
    def failure_reason(self) -> str: return "forbids::configured_to_hide_all_compounds"

    @staticmethod
    def for_if(match: Match) -> ForbidsConfiguredToHideCompounds | None:
        if ConfigurationCache.hide_all_compounds() and match.inspector.word.is_custom_compound:
            if match.inspector.is_ichidan_covering_godan_potential:  # we can't tell whether it is really the potential or the ichidan in this case, so we show both
                return None
            else:
                return _instance

        return None

_instance = ForbidsConfiguredToHideCompounds()
