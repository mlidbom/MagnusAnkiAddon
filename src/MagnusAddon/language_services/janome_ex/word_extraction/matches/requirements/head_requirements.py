from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from language_services.janome_ex.word_extraction.analysis_constants import non_word_characters
from sysutils import kana_utils
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from sysutils.weak_ref import WeakRef

class HeadRequirements(Slots):
    _te_forms = {"て", "って", "で"}
    def __init__(self, match: VocabMatch, word_variant: WeakRef[CandidateWordVariant], end_of_stem: WeakRef[TextAnalysisLocation] | None) -> None:
        rules = match.vocab.matching_configuration
        self.config = rules

        self.has_prefix = end_of_stem is not None and end_of_stem().token.surface != "" and end_of_stem().token.surface[-1] not in non_word_characters
        self.fulfills_is_strictly_suffix = not rules.is_strictly_suffix.is_set() or self.has_prefix

        self.fulfills_required_prefix = (not rules.configurable_rules.required_prefix.get()
                                         or (end_of_stem is not None and self.has_prefix and any(required for required in rules.configurable_rules.required_prefix.get() if end_of_stem().token.surface.endswith(required))))

        self.fulfills_prefix_not = (not rules.configurable_rules.prefix_is_not.get()
                                    or not self.has_prefix
                                    or (end_of_stem is not None and not any(forbidden for forbidden in rules.configurable_rules.prefix_is_not.get() if end_of_stem().token.surface.endswith(forbidden))))

        self.has_a_stem = end_of_stem is not None and end_of_stem().token.surface[-1] in conjugator.a_stem_characters
        self.fulfills_forbids_a_stem_requirement = not rules.a_stem.is_forbidden or not self.has_a_stem
        self.fulfills_requires_a_stem = not rules.a_stem.is_required or self.has_a_stem

        self.has_past_tense_stem = end_of_stem is not None and (end_of_stem().token.is_past_tense_stem() or word_variant().word.start_location.token.is_past_tense_marker())
        self.fulfills_forbids_past_tense_stem = not rules.past_tense_stem.is_forbidden or not self.has_past_tense_stem
        self.fulfills_requires_past_tense_stem = not rules.past_tense_stem.is_required or self.has_past_tense_stem

        # todo: get this stuff moved into the tokenizing stage...
        self.has_t_form_stem = (end_of_stem is not None
                                and not end_of_stem().token.is_special_nai_negative()  # todo: review: this code means that we do not consider ない to be a te form stem, but it seems that janome does.....
                                and (end_of_stem().token.is_t_form_stem()
                                     or (end_of_stem().token.is_past_tense_stem() and any(tform for tform in HeadRequirements._te_forms if match.parsed_form.startswith(tform)))
                                     or (end_of_stem().token.is_ichidan_masu_stem() and any(tform for tform in HeadRequirements._te_forms if match.parsed_form.startswith(tform)))))
        self.fulfills_requires_t_form_stem = not rules.t_form_stem.is_required or self.has_t_form_stem
        self.fulfills_forbids_t_form_stem = not rules.t_form_stem.is_forbidden or not self.has_t_form_stem

        self.has_e_stem = (end_of_stem is not None and
                           (end_of_stem().token.surface[-1] in conjugator.e_stem_characters
                            or kana_utils.character_is_kanji(end_of_stem().token.surface[-1])))

        self.fulfills_requires_e_stem_requirement = not rules.e_stem.is_required or self.has_e_stem
        self.fulfills_forbids_e_stem_requirement = not rules.e_stem.is_forbidden or not self.has_e_stem

        self.are_fulfilled = (True
                              and self.fulfills_is_strictly_suffix
                              and self.fulfills_required_prefix
                              and self.fulfills_prefix_not
                              and self.fulfills_forbids_a_stem_requirement
                              and self.fulfills_requires_a_stem
                              and self.fulfills_requires_e_stem_requirement
                              and self.fulfills_forbids_e_stem_requirement
                              and self.fulfills_requires_past_tense_stem
                              and self.fulfills_forbids_past_tense_stem
                              and self.fulfills_requires_t_form_stem
                              and self.fulfills_forbids_t_form_stem
                              )

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.fulfills_is_strictly_suffix, "is_strictly_suffix")
                .append_if(not self.fulfills_required_prefix, "required_prefix")
                .append_if(not self.fulfills_prefix_not, "prefix_not")
                .append_if(not self.fulfills_forbids_a_stem_requirement, "forbids_a_stem")
                .append_if(not self.fulfills_requires_a_stem, "requires_a_stem")
                .append_if(not self.fulfills_forbids_e_stem_requirement, "forbids_e_stem")
                .append_if(not self.fulfills_requires_e_stem_requirement, "requires_e_stem")
                .append_if(not self.fulfills_forbids_past_tense_stem, "forbids_past_tense_stem")
                .append_if(not self.fulfills_requires_past_tense_stem, "requires_past_tense_stem")
                .append_if(not self.fulfills_forbids_t_form_stem, "forbids_t_form_stem")
                .append_if(not self.fulfills_requires_t_form_stem, "requires_t_form_stem")
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())
