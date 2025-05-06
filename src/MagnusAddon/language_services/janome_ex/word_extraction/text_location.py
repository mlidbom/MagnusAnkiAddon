from __future__ import annotations
from typing import TYPE_CHECKING

from language_services import conjugator
from note.note_constants import Mine
from sysutils import ex_sequence
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from note.vocabnote import VocabNote
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm

from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken, SplitToken

from typing import Optional

from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_max_lookahead = 12

class TokenTextLocation:
    def __init__(self, analysis: TextAnalysis, token: ProcessedToken, character_start_index: int, token_index: int):
        surface = token.surface
        base = token.base_form
        self.is_covered_by: Optional[TokenTextLocation] = None
        self.token: ProcessedToken = token
        self.analysis: TextAnalysis = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(surface) - 1
        self.surface: str = surface
        self.base: str = base

        self.word_candidates: list[CandidateWord] = []
        self.valid_candidates: list[CandidateWord] = []
        self.display_words: list[CandidateForm] = []
        self.all_words: list[CandidateForm] = []
        self.all_candidates: list[CandidateWord] = []

    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.surface} | {self.base})
{newline.join([cand.__repr__() for cand in self.word_candidates])}
"""

    def forward_list(self, length: int = 99999) -> list[TokenTextLocation]:
        list = self.analysis.locations[self.token_index: self.token_index + length + 1]
        return list

    def run_analysis_step_1(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.all_candidates = [CandidateWord(self.forward_list(index)) for index in range(lookahead_max - 1, -1, -1)]
        self.all_candidates[-1].complete_analysis()  # the non-compound part needs to be completed first

    def run_analysis_step_2(self) -> None:
        for cand in self.all_candidates[:-1]:  # we already have the last one completed
            cand.complete_analysis()

        self.word_candidates = [word for word in self.all_candidates if word.is_word]
        self.valid_candidates = [word for word in self.all_candidates if word.has_valid_candidates()]

        if self.valid_candidates and self.is_covered_by is None:
            self.display_words = self.valid_candidates[0].display_words
            self.display_words = [covered for covered in self.display_words
                                  if not any([covering for covering in self.display_words if covered.form in covering.form and covered != covering])]

            covering_forward_count = self.valid_candidates[0].length - 1
            for location in self.forward_list(covering_forward_count)[1:]:
                location.is_covered_by = self

        self.all_words = ex_sequence.flatten([v.display_words for v in self.valid_candidates])

    def next(self) -> Optional[TokenTextLocation]:
        if len(self.analysis.locations) > self.token_index + 1:
            return self.analysis.locations[self.token_index + 1]
        return None

    def previous(self) -> Optional[TokenTextLocation]:
        if self.token_index > 0:
            return self.analysis.locations[self.token_index -1]
        return None

    def is_next_location_inflecting_word(self) -> bool:
        next = self.next()
        return next is not None and next.is_inflecting_word()

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
