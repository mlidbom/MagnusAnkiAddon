from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.ui.web.sentence.candidate_word_variant_viewmodel import CandidateWordVariantViewModel

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from jastudio.ui.web.sentence.match_viewmodel import MatchViewModel
    from typed_linq_collections.collections.q_list import QList


class TextAnalysisViewModel(Slots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = text_analysis
        self.candidate_words: QList[CandidateWordVariantViewModel] = text_analysis.indexing_word_variants.select(CandidateWordVariantViewModel).to_list()
        variant_view_models: QList[CandidateWordVariantViewModel] = self.candidate_words
        matches: QList[MatchViewModel] = variant_view_models.select_many(lambda variant_vm: variant_vm.matches).to_list()
        self.displayed_matches:QList[MatchViewModel] = matches.where(lambda match: match.is_displayed).to_list()
