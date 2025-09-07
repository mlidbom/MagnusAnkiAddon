from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant

from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
from note.sentences.sentence_configuration import SentenceConfiguration
from sysutils import ex_sequence

_tokenizer = JNTokenizer()

class TextAnalysis(WeakRefable,Slots):
    version = "text_analysis_0.1"

    def __init__(self, sentence: str, sentence_configuration: SentenceConfiguration) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.weakref = WeakRef(self)
        self.text = sentence
        self.configuration = sentence_configuration
        self.tokenized_text = _tokenizer.tokenize(sentence)
        self.pre_processed_tokens: list[ProcessedToken] = self.tokenized_text.pre_process()

        self.locations: list[TextAnalysisLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.pre_processed_tokens):
            self.locations.append(TextAnalysisLocation(self.weakref, token, character_index, token_index))
            character_index += len(token.surface)

        self.start_location = self.locations[0]
        self._connect_next_and_previous_to_locations()
        self._analysis_step_1_analyze_non_compound()
        self._analysis_step_2_analyze_compounds()
        self._analysis_step_3_analyze_display_status()
        self._analysis_step_4_create_collections()
        self._analysis_step_5_calculate_preference_between_overlapping_display_candidates()

        self.all_word_variants: list[CandidateWordVariant] = ex_sequence.flatten([loc.all_word_variants for loc in self.locations])
        self.valid_word_variants: list[CandidateWordVariant] = ex_sequence.flatten([loc.valid_variants for loc in self.locations])
        self.display_word_variants: list[CandidateWordVariant] = ex_sequence.flatten([loc.display_variants for loc in self.locations])

    @classmethod
    def from_text(cls, text: str) -> TextAnalysis:
        return cls(text, SentenceConfiguration.empty())

    def all_words_strings(self) -> list[str]:
        return [w.form for w in self.valid_word_variants]

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

    def _analysis_step_3_analyze_display_status(self) -> None:
        for location in self.locations:
            location.analysis_step_3_analyze_display_status()

    def _analysis_step_4_create_collections(self) -> None:
        for location in self.locations:
            location.analysis_step_4_create_collections()

    def _analysis_step_5_calculate_preference_between_overlapping_display_candidates(self) -> None:
        # for location in self.locations:
        #     location.analysis_step_5_calculate_preference_between_overlapping_display_variant5()
        changes_made = True
        while changes_made:
            changes_made = False
            for location in self.locations:
                changes_made = changes_made or location.analysis_step_5_calculate_preference_between_overlapping_display_variant5()
