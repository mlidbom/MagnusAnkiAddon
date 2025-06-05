from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils import ex_sequence
from ui.web.sentence.candidate_word_variant_viewmodel import CandidateWordVariantViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from ui.web.sentence.match_viewmodel import MatchViewModel


class TextAnalysisViewModel(Slots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = text_analysis
        self.candidate_words: list[CandidateWordVariantViewModel] = [CandidateWordVariantViewModel(candidate_word) for candidate_word in text_analysis.all_word_variants]
        variant_view_models: list[CandidateWordVariantViewModel] = self.candidate_words
        matches: list[MatchViewModel] = ex_sequence.flatten([cand.matches for cand in variant_view_models])
        self.displayed_matches:list[MatchViewModel] = [display_form for display_form in matches if display_form.is_displayed]
