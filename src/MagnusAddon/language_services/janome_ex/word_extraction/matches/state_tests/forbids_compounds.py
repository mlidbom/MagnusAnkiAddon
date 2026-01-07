from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from configuration.configuration_cache_impl import ConfigurationCache
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsConfiguredToHideCompounds(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("configured_to_hide_all_compounds")

    @classmethod
    def apply_to(cls, match: Match) -> MatchRequirement | None:
        if (ConfigurationCache.hide_all_compounds()
                and match.inspector.word.is_compound
                and match.word.analysis.for_ui
                and match.inspector.compound_locations_all_have_valid_non_compound_matches
                and not match.inspector.is_verb_dictionary_form_compound
                and not match.inspector.is_ichidan_covering_godan_potential):  # we can't tell whether it is really the potential or the ichidan in this case, so we don't hide those "compounds"
            return ForbidsConfiguredToHideCompounds._failed

        return None
