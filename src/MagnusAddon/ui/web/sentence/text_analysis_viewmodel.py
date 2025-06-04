from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils import ex_sequence
from ui.web.sentence.candidate_word_viewmodel import CandidateWordViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from ui.web.sentence.display_form_viewmodel import DisplayFormViewModel


class TextAnalysisViewModel(Slots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = text_analysis
        self.candidate_words: list[CandidateWordViewModel] = [CandidateWordViewModel(candidate_word) for candidate_word in text_analysis.all_word_variants]
        candidate_words: list[CandidateWordViewModel] = self.candidate_words
        display_forms: list[DisplayFormViewModel] = ex_sequence.flatten([cand.display_forms for cand in candidate_words])
        self.displayed_forms:list[DisplayFormViewModel] = [display_form for display_form in display_forms if display_form.is_displayed]
