from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TokenTextLocation
from sysutils import ex_sequence
from sysutils.ex_str import newline

_tokenizer = JNTokenizer()

class TextAnalysis:
    version = "text_analysis_0.1"

    def __init__(self, sentence:str, exclusions:set[WordExclusion]) -> None:
        self.text = sentence
        self.exclusions = exclusions
        self.tokens:list[ProcessedToken] = _tokenizer.tokenize(sentence).pre_process()

        self.locations:list[TokenTextLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.tokens):
            self.locations.append(TokenTextLocation(WeakRef(self), token, character_index, token_index))
            character_index += len(token.surface)

        self.start_location = self.locations[0]

        for location in self.locations:
            location.run_analysis_step_1()

        for location in self.locations:
            location.run_analysis_step_2()

        self.display_words:list[CandidateForm] = ex_sequence.flatten([loc.display_words for loc in self.locations])
        self.all_words: list[CandidateForm] = ex_sequence.flatten([loc.all_words for loc in self.locations])

        self.display_forms = ex_sequence.flatten([w.display_forms for w in self.display_words])


    def __repr__(self) -> str:
        return f"""{self.text}
{newline.join([dw.__repr__() for dw in self.display_words])}
"""