from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from typing import Optional

from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.word_extraction import text_navigator
from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_noise_characters = {'.',',',':',';','/','|','。','、'}
_max_lookahead = 12

class TextLocation:
    def __init__(self, analysis:TextAnalysis, start_index:int, surface:str, base:str):
        self.analysis = analysis
        self.start_index = start_index
        self.end_index = start_index + len(surface) - 1
        self.surface = surface
        self.base = base
        self.previous: Optional[TextLocation] = None
        self.next: Optional[TextLocation] = None
        self.candidate_words: list[CandidateWord] = []

    def __repr__(self) -> str:
        return f"""
TextLocation('{self.start_index}-{self.end_index}, {self.surface} | {self.base}  prev.start:{self.previous.start_index if self.previous else None}, next.start:{self.next.start_index if self.next else None})
#####
{newline.join([cand.__repr__() for cand in self.candidate_words])}
####
"""

    def _forward_list(self, length:int) -> list[TextLocation]:
        return text_navigator.forward_list(self, length)

    def run_analysis(self) -> None:
        lookahead_max = min(_max_lookahead, len(self._forward_list(_max_lookahead)))

        self.candidate_words = []
        for index in range(lookahead_max - 1, -1, -1):
            self.candidate_words.append(CandidateWord(self._forward_list(index)))

        if self.next:
            self.next.run_analysis()

class TokenTextLocation(TextLocation):
    def __init__(self, analysis:TextAnalysis, token: JNToken, start_index:int):
        super().__init__(analysis, start_index, token.surface, token.base_form)
        self.token = token
