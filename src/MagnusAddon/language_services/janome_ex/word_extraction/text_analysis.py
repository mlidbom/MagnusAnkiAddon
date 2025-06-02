from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant

from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
from note.sentences.sentence_configuration import SentenceConfiguration
from sysutils import ex_sequence

_tokenizer = JNTokenizer()

class TextAnalysis(Slots):
    __slots__ = ["__weakref__"]
    version = "text_analysis_0.1"

    def __init__(self, sentence: str, sentence_configuration: SentenceConfiguration) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.weakref = WeakRef(self)
        self.text = sentence
        self.configuration = sentence_configuration
        self.tokens: list[ProcessedToken] = _tokenizer.tokenize(sentence).pre_process()

        self.locations: list[TextAnalysisLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.tokens):
            self.locations.append(TextAnalysisLocation(self.weakref, token, character_index, token_index))
            character_index += len(token.surface)

        self.start_location = self.locations[0]
        self._connect_next_and_previous_to_locations()
        self._analysis_step_1_analyze_non_compound()
        self._analysis_step_2_analyze_compounds()
        self._analysis_step_3_calculate_preference_between_overlapping_valid_candidates()

        self.valid_variants: list[CandidateWordVariant] = ex_sequence.flatten([loc.valid_variants for loc in self.locations])
        self.display_variants: list[CandidateWordVariant] = ex_sequence.flatten([loc.display_variants for loc in self.locations])

    @classmethod
    def from_text(cls, text: str) -> TextAnalysis:
        return cls(text, SentenceConfiguration.empty())

    def all_words_strings(self) -> list[str]:
        return [w.form for w in self.valid_variants]

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
            location.analysis_step_1_analyze_non_compound()

    def _analysis_step_2_analyze_compounds(self) -> None:
        for location in self.locations:
            location.analysis_step_2_analyze_compounds()

    def _analysis_step_3_calculate_preference_between_overlapping_valid_candidates(self) -> None:
        for location in self.locations:
            location.analysis_step_3_calculate_preference_between_overlapping_valid_candidates()
