from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsCompositionallyTransparentCompound(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("configured_to_hide_compositionally_transparent_compounds")

    @staticmethod
    def apply_to(inspector: VocabMatchInspector) -> MatchRequirement | None:
        _match = inspector.match
        if (ConfigurationCache.hide_transparent_compounds()
                and _match.word.analysis.for_ui
                and _match.word.is_compound
                and inspector.compound_locations_all_have_valid_non_compound_matches
                and _match.vocab.matching_configuration.bool_flags.is_compositionally_transparent_compound.is_set()):
            return ForbidsCompositionallyTransparentCompound._failed
        return None
