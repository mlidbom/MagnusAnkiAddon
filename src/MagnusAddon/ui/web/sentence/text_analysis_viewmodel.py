from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from ui.web.sentence.candidate_word_viewmodel import CandidateWordViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis


class TextAnalysisViewModel(Slots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = text_analysis
        self.candidate_words: list[CandidateWordViewModel] = [CandidateWordViewModel(candidate_word) for candidate_word in text_analysis.valid_word_variants]
