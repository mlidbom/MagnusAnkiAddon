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
        # Phase 1: Resolve yield chains by processing right-to-left.
        # Words can only yield to words starting AFTER them (or overlapping but extending beyond).
        # By processing right-to-left, when we evaluate a word's yield status, all potential
        # yield targets have already been resolved, so we see their final display state.
        for location in reversed(self.locations):
            location.run_display_analysis_and_update_display_words()

        # Phase 2: Resolve shadowing by processing left-to-right.
        # Longer words shadow shorter words at the same or following positions.
        # By processing left-to-right, when a word is chosen for display, it shadows
        # forward positions before they're processed.
        for location in self.locations:
            location.resolve_shadowing_for_display_word()

        # Phase 3: Final cleanup - re-run display analysis with shadowing applied.
        # This ensures display_variants and display_words correctly reflect shadowed state.
        # We bound iterations for safety, though typically only 1-2 passes are needed.
        max_iterations = 10
        for _ in range(max_iterations):
            changes_made = False
            for location in reversed(self.locations):
                if location.run_display_analysis_and_update_display_words():
                    changes_made = True
            if not changes_made:
                break
