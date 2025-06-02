from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWordVariant

from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TokenTextLocation
from note.sentences.sentence_configuration import SentenceConfiguration
from sysutils import ex_sequence

_tokenizer = JNTokenizer()

class TextAnalysis(Slots):
    __slots__ = ["__weakref__"]
    version = "text_analysis_0.1"

    def __init__(self, sentence: str, sentence_configuration: SentenceConfiguration) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.text = sentence
        self.configuration = sentence_configuration
        self.tokens: list[ProcessedToken] = _tokenizer.tokenize(sentence).pre_process()

        self.locations: list[TokenTextLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.tokens):
            self.locations.append(TokenTextLocation(WeakRef(self), token, character_index, token_index))
            character_index += len(token.surface)

        self.start_location = self.locations[0]

        for location in self.locations:
            location.analysis_step_1_connect_next_and_previous()

        for location in self.locations:
            location.analysis_step_2_analyze_non_compound()

        for location in self.locations:
            location.analysis_step_3_analyze_compounds()

        for location in self.locations:
            location.analysis_step_4_calculate_preference_between_overlapping_valid_candidates()

        self.display_words: list[CandidateWordVariant] = ex_sequence.flatten([loc.display_variants for loc in self.locations])
        self.all_words: list[CandidateWordVariant] = ex_sequence.flatten([loc.all_words for loc in self.locations])

    @classmethod
    def from_text(cls, text: str) -> TextAnalysis:
        return cls(text, SentenceConfiguration.empty())

    def all_words_strings(self) -> list[str]:
        return [w.form for w in self.all_words]

    def __repr__(self) -> str:
        return self.text
