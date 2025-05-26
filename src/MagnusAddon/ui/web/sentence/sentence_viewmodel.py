from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_form import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word import TokenRange
    from note.sentences.sentencenote import SentenceNote

class CandidateFormViewModel:
    def __init__(self, candidate_form: CandidateWord) -> None:
        self.candidate_form = candidate_form

class CandidateWordViewModel(Slots):
    def __init__(self, candidate_word: TokenRange) -> None:
        self.candidate_word = candidate_word

    def display_words(self) -> list[CandidateFormViewModel]: return [CandidateFormViewModel(candidate_form) for candidate_form in self.candidate_word.all_words]

class TextAnalysisViewModel(Slots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis = text_analysis
        self.candidate_words = [CandidateFormViewModel(candidate_word) for candidate_word in text_analysis.all_words]

class SentenceViewModel(Slots):
    def __init__(self, sentence: SentenceNote) -> None:
        self.sentence = sentence
        self.analysis = TextAnalysisViewModel(TextAnalysis(sentence.get_question(), sentence.configuration.configuration))