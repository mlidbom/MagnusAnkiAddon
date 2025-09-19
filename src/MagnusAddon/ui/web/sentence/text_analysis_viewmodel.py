from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots
from ui.web.sentence.candidate_word_variant_viewmodel import CandidateWordVariantViewModel

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from sysutils.collections.queryable.collections.q_list import QList
    from ui.web.sentence.match_viewmodel import MatchViewModel


class TextAnalysisViewModel(AutoSlots):
    def __init__(self, text_analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = text_analysis
        self.candidate_words: QList[CandidateWordVariantViewModel] = text_analysis.indexing_word_variants.select(CandidateWordVariantViewModel).to_list() #[CandidateWordVariantViewModel(candidate_word) for candidate_word in text_analysis.all_word_variants]
        variant_view_models: QList[CandidateWordVariantViewModel] = self.candidate_words
        matches: QList[MatchViewModel] = variant_view_models.select_many(lambda variant_vm: variant_vm.matches).to_list() #ex_sequence.flatten([cand.matches for cand in variant_view_models])
        self.displayed_matches:QList[MatchViewModel] = matches.where(lambda match: match.is_displayed).to_list() #[display_form for display_form in matches if display_form.is_displayed]
