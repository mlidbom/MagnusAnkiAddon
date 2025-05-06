from __future__ import annotations
from typing import TYPE_CHECKING

from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

from sysutils.ex_str import newline
from sysutils import ex_sequence
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TokenTextLocation
_tokenizer = JNTokenizer()

class TextAnalysis:
    version = "text_analysis_0.1"

    def __init__(self, sentence:str, exclusions:list[WordExclusion]):
        self.text = sentence
        self.exclusions = exclusions
        print(f"exclusions: {exclusions}")
        self.tokens:list[ProcessedToken] = _tokenizer.tokenize(sentence).pre_process()

        locations:list[TokenTextLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.tokens):
            locations.append(TokenTextLocation(self, token, character_index))
            character_index += len(token.surface)

        for index, location in enumerate(locations[1:]):
            locations[index].next = location
            location.previous = locations[index]

        self.start_location = locations[0]

        self.start_location.run_analysis_step_0_split_potential_verbs()
        self.start_location.run_analysis_step_1()
        self.start_location.run_analysis_step_2()

        self.locations = self.start_location.forward_list()
        self.display_words:list[CandidateForm] = ex_sequence.flatten([loc.display_words for loc in self.locations])
        self.all_words: list[CandidateForm] = ex_sequence.flatten([loc.all_words for loc in self.locations])

        self.display_forms = ex_sequence.flatten([w.display_forms for w in self.display_words])


    def __repr__(self) -> str:
        return f"""{self.text}
{newline.join([dw.__repr__() for dw in self.display_words])}
"""