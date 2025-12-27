from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.processed_token import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.match import Match

from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
from note.sentences.sentence_configuration import SentenceConfiguration

_tokenizer = JNTokenizer()

@final
class TextAnalysis(WeakRefable, Slots):
    version = "text_analysis_0.1"

    def __init__(self, sentence: str, sentence_configuration: SentenceConfiguration) -> None:
        self.weakref = WeakRef(self)
        self.text = sentence
        self.configuration = sentence_configuration
        self.tokenized_text = _tokenizer.tokenize(sentence)
        self.pre_processed_tokens: QList[ProcessedToken] = self.tokenized_text.pre_process()

        self.locations: QList[TextAnalysisLocation] = QList()

        character_index = 0
        for token_index, token in enumerate(self.pre_processed_tokens):
            self.locations.append(TextAnalysisLocation(self.weakref, token, character_index, token_index))
            character_index += len(token.surface)

        self.start_location = self.locations[0]
        self._connect_next_and_previous_to_locations()
        self._analysis_step_1_analyze_non_compound()
        self._analysis_step_2_analyze_compounds()
        self._analysis_step_3_run_initial_display_analysis()
        self._analysis_step_5_calculate_preference_between_overlapping_display_candidates()

        self.all_matches: QList[Match] = (self.locations
                                          .select_many(lambda location: location.candidate_words)
                                          .select_many(lambda candidate: candidate.all_matches)
                                          .to_list())

        self.indexing_word_variants: QList[CandidateWordVariant] = self.locations.select_many(lambda location: location.indexing_variants).to_list()
        self.valid_word_variants: QList[CandidateWordVariant] = self.locations.select_many(lambda location: location.valid_variants).to_list()
        self.display_word_variants: QList[CandidateWordVariant] = self.locations.select_many(lambda location: location.display_variants).to_list()

        self.indexing_matches: QList[Match] = self.indexing_word_variants.select_many(lambda variant: variant.matches).to_list()
        self.valid_word_variant_matches: QList[Match] = self.valid_word_variants.select_many(lambda variant: variant.matches).to_list()
        # todo: bug valid_matches here and valid_word_variant_valid_matches should be identical. Once they are, the valid_word_variant_valid_matches collection should be removed
        self.valid_matches: QList[Match] = self.indexing_matches.where(lambda match: match.is_valid).to_list()
        self.valid_word_variant_valid_matches: QList[Match] = self.valid_word_variant_matches.where(lambda match: match.is_valid).to_list()
        self.display_matches: QList[Match] = self.indexing_matches.where(lambda match: match.is_displayed).to_list()

    @classmethod
    def from_text(cls, text: str) -> TextAnalysis:
        return cls(text, SentenceConfiguration.empty())

    def all_words_strings(self) -> list[str]:
        return [w.form for w in self.valid_word_variants]
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

    def _analysis_step_3_run_initial_display_analysis(self) -> None:
        for location in self.locations:
            location.analysis_step_3_run_initial_display_analysis()

    def _analysis_step_5_calculate_preference_between_overlapping_display_candidates(self) -> None:
        changes_made = True
        while changes_made:
            changes_made = False
            for location in self.locations:
                if location.analysis_step_5_resolve_chains_of_compounds_yielding_to_the_next_compound_pass_true_if_there_were_changes():
                    changes_made = True
