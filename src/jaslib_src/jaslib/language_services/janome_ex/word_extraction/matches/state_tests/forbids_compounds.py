# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# from autoslot import Slots
#
# from jaslib.configuration.settings import Settings
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
#
# if TYPE_CHECKING:
#     from jaslib.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
#
# class ForbidsConfiguredToHideAllCompounds(Slots):
#     _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("configured_to_hide_all_compounds")
#
#     @classmethod
#     def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
#         if (Settings.hide_all_compounds()
#                 and inspector.word.is_compound
#                 and inspector.word.analysis.for_ui
#                 and inspector.compound_locations_all_have_valid_non_compound_matches
#                 and not inspector.is_verb_dictionary_form_compound
#                 and not inspector.is_ichidan_covering_godan_potential):  # we can't tell whether it is really the potential or the ichidan in this case, so we don't hide those "compounds"
#             return ForbidsConfiguredToHideAllCompounds._failed
#
#         return None
