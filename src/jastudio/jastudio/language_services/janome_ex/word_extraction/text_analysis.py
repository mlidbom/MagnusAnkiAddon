from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from jastudio.sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.q_iterable import query  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from jastudio.language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from jastudio.language_services.janome_ex.word_extraction.matches.match import Match
    from typed_linq_collections.collections.q_list import QList

from jastudio.language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from jastudio.language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
from jastudio.note.sentences.sentence_configuration import SentenceConfiguration

_tokenizer = JNTokenizer()

@final
class TextAnalysis(WeakRefable, Slots):
    version = "text_analysis_0.1"

    def __init__(self, sentence: str, sentence_configuration: SentenceConfiguration, for_ui: bool = False) -> None:
        self.weakref = WeakRef(self)
        self.for_ui = for_ui
        self.text = sentence
        self.configuration = sentence_configuration
        self.tokenized_text = _tokenizer.tokenize(sentence)
        self.pre_processed_tokens: list[IAnalysisToken] = self.tokenized_text.pre_process()

        self.locations: list[TextAnalysisLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.pre_processed_tokens):
            self.locations.append(TextAnalysisLocation(self.weakref, token, character_index, token_index))
            character_index += len(token.surface)

        self.start_location = self.locations[0]
        self._connect_next_and_previous_to_locations()
        self._analysis_step_1_analyze_non_compound()
        self._analysis_step_2_analyze_compounds()
        self._analysis_step_3_run_display_analysis_without_shadowing_information_so_that_all_valid_matches_are_displayed_and_can_be_accounted_for_in_yielding_to_upcoming_compounds_return_true_on_changes()
        if self._analysis_step_4_set_initial_shadowing_state_return_true_on_changes():
            self._analysis_step_5_calculate_preference_between_overlapping_display_candidates()

        self.indexing_word_variants: QList[CandidateWordVariant] = query(self.locations).select_many(lambda location: location.indexing_variants).to_list()
        self.display_word_variants: QList[CandidateWordVariant] = query(self.locations).select_many(lambda location: location.display_variants).to_list()

        self.valid_matches: QList[Match] = self.indexing_word_variants.select_many(lambda variant: variant.valid_matches).to_list()
        self.display_matches: QList[Match] = self.display_word_variants.select_many(lambda variant: variant.display_matches).to_list()

    @classmethod
    def from_text(cls, text: str) -> TextAnalysis:
        return cls(text, SentenceConfiguration.empty())

    def all_words_strings(self) -> list[str]:
        return [w.parsed_form for w in self.valid_matches]
    @override
    def __repr__(self) -> str:
        return self.text

    def _connect_next_and_previous_to_locations(self) -> None:
        for token_index, location in enumerate(self.locations):
            if len(self.locations) > token_index + 1:
                location.next = self.locations[token_index + 1].weakref

            if token_index > 0:
                location.previous = self.locations[token_index - 1].weakref

    def _analysis_step_1_analyze_non_compound(self) -> None:
        for location in self.locations:
            location.analysis_step_1_analyze_non_compound_validity()

    def _analysis_step_2_analyze_compounds(self) -> None:
        for location in self.locations:
            location.analysis_step_2_analyze_compound_validity()

    def _analysis_step_3_run_display_analysis_without_shadowing_information_so_that_all_valid_matches_are_displayed_and_can_be_accounted_for_in_yielding_to_upcoming_compounds_return_true_on_changes(self) -> None:
        for location in self.locations:
            location.analysis_step_3_run_display_analysis_without_shadowing_information_so_that_all_valid_matches_are_displayed_and_can_be_accounted_for_in_yielding_to_upcoming_compounds()

    def _analysis_step_4_set_initial_shadowing_state_return_true_on_changes(self) -> bool:
        change_made = False
        for location in self.locations:
            if location.analysis_step_4_set_initial_shadowing_and_recalculate_display_words_return_true_on_changes():
                change_made = True
        return change_made

    def _analysis_step_5_calculate_preference_between_overlapping_display_candidates(self) -> None:
        changes_made = True
        while changes_made:
            changes_made = False
            for location in self.locations:
                if location.analysis_step_5_update_shadowing_and_recalculate_display_words_return_true_on_changes():
                    changes_made = True
