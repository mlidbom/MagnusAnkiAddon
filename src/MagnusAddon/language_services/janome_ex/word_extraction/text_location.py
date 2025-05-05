from __future__ import annotations
from typing import TYPE_CHECKING

from note.note_constants import Mine

if TYPE_CHECKING:
    from note.vocabnote import VocabNote
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm

from typing import Optional

from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.word_extraction import text_navigator
from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_noise_characters = {'.', ',', ':', ';', '/', '|', '。', '、'}
_max_lookahead = 12



class TokenTextLocation:
    def __init__(self, analysis: TextAnalysis, token: JNToken, start_index: int):
        surface = token.surface
        base = token.base_form
        self.is_covered_by: Optional[TokenTextLocation] = None
        self.token:JNToken = token
        self.analysis:TextAnalysis = analysis
        self.start_index:int = start_index
        self.end_index:int = start_index + len(surface) - 1
        self.surface:str = surface
        self.base:str = base
        self.previous: Optional[TokenTextLocation] = None
        self.next: Optional[TokenTextLocation] = None

        self.all_candidates: list[CandidateWord] = []
        self.word_candidates: list[CandidateWord] = []
        self.valid_candidates: list[CandidateWord] = []
        self.display_words: list[CandidateForm] = []

    def __repr__(self) -> str:
        return f"""
TextLocation('{self.start_index}-{self.end_index}, {self.surface} | {self.base}  prev.start:{self.previous.start_index if self.previous else None}, next.start:{self.next.start_index if self.next else None})
{newline.join([cand.__repr__() for cand in self.word_candidates])}
"""

    def forward_list(self, length: int = 99999) -> list[TokenTextLocation]:
        return text_navigator.forward_list(self, length)

    def run_analysis(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.all_candidates = [CandidateWord(self.forward_list(index)) for index in range(lookahead_max - 1, -1, -1)]

        self.all_candidates.sort(key=lambda cand: cand.length, reverse=True)#we need the shortest parts initialized first, that's why the reverse afterwards.
        self.word_candidates = [word for word in self.all_candidates if word.is_word]
        self.valid_candidates = [word for word in self.all_candidates if word.has_valid_candidates()]

        if self.valid_candidates and self.is_covered_by is None:
            self.display_words = self.valid_candidates[0].display_words
            covering_forward_count = self.valid_candidates[0].length - 1
            for location in self.forward_list(covering_forward_count)[1:]:
                location.is_covered_by = self


        if self.next:
            self.next.run_analysis()

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next.is_inflecting_word()

    def is_inflecting_word(self) -> bool:
        def lookup_vocabs_prefer_exact_match(form: str) -> list[VocabNote]:
            from ankiutils import app
            matches: list[VocabNote] = app.col().vocab.with_form(form)
            exact_match = [voc for voc in matches if voc.get_question_without_noise_characters() == form]
            return exact_match if exact_match else matches

        vocab = lookup_vocabs_prefer_exact_match(self.base)
        if any([voc for voc in vocab if voc.has_tag(Mine.Tags.inflecting_word)]):
            return True

        return False

    def is_inflected_word(self) -> bool:
        return self.next is not None and self.token.is_inflectable_word() and self.next.is_inflecting_word()