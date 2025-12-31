from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.processed_token import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_max_lookahead = 12  # In my collection the longest so far is 9, so 12 seems a pretty good choice.

@final
class TextAnalysisLocation(WeakRefable, Slots):
    def __init__(self, analysis: WeakRef[TextAnalysis], token: ProcessedToken, character_start_index: int, token_index: int) -> None:
        self.weakref = WeakRef(self)
        self.next: WeakRef[TextAnalysisLocation] | None = None
        self.previous: WeakRef[TextAnalysisLocation] | None = None
        self.token: ProcessedToken = token
        self.is_shadowed_by: QList[WeakRef[TextAnalysisLocation]] = QList()
        self.shadows: QList[WeakRef[TextAnalysisLocation]] = QList()
        self.analysis: WeakRef[TextAnalysis] = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(self.token.surface) - 1

        self.display_variants: QList[CandidateWordVariant] = QList()
        self.indexing_variants: QList[CandidateWordVariant] = QList()
        self.candidate_words: QList[CandidateWord] = QList()
        self.display_words: QList[CandidateWord] = QList()

    @override
    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.token.surface} | {self.token.base_form})
{newline.join([cand.__repr__() for cand in self.indexing_variants])}
"""

    def forward_list(self, length: int = 99999) -> QList[TextAnalysisLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    def analysis_step_1_analyze_non_compound_validity(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.candidate_words = QList(CandidateWord(self.forward_list(index).select(lambda it: it.weakref).to_list()) for index in range(lookahead_max - 1, -1, -1))
        self.candidate_words[-1].run_validity_analysis()  # the non-compound part needs to be completed first

    def analysis_step_2_analyze_compound_validity(self) -> None:
        for range_ in self.candidate_words[:-1]:  # we already have the last one completed
            range_.run_validity_analysis()

        self.indexing_variants = self.candidate_words.select_many(lambda candidate: candidate.indexing_variants).to_list()

    def run_display_analysis_and_update_display_words_pass_true_if_there_were_changes(self) -> bool:
        changes_made = False
        for range_ in self.candidate_words:
            if range_.run_display_analysis_pass_true_if_there_were_changes():
                changes_made = True

        if changes_made:
            self.display_words = self.candidate_words.where(lambda it: it.display_variants.any()).to_list()
        return changes_made

    def analysis_step_3_run_display_analysis_without_shadowing_information_so_that_all_valid_matches_are_displayed_and_can_be_accounted_for_in_yielding_to_upcoming_compounds(self) -> None:
        self.run_display_analysis_and_update_display_words_pass_true_if_there_were_changes()

    def analysis_step_5_recalculate_display_words_based_on_current_shadowing_and_yielding_return_true_if_there_were_changes(self, initial_run: bool = False) -> bool:
        display_words_updated = self.run_display_analysis_and_update_display_words_pass_true_if_there_were_changes()
        if initial_run or display_words_updated:
            self.update_shadowing()
        return display_words_updated

    def update_shadowing(self) -> None:
        if self.display_words and not any(self.is_shadowed_by):
            self.display_variants = self.display_words[0].display_variants

            covering_forward_count = self.display_words[0].location_count - 1
            for shadowed in self.forward_list(covering_forward_count)[1:]:
                shadowed.is_shadowed_by.append(self.weakref)
                self.shadows.append(shadowed.weakref)
                shadowed._clear_shadowed()
        else:
            self._clear_shadowed()

    def _clear_shadowed(self) -> None:
        for shadowed_shadowed in self.shadows:
            shadowed_shadowed().is_shadowed_by.remove(self.weakref)
        self.shadows.clear()

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next().is_inflecting_word()

    # todo: having this check here only means that marking a compound as an inflecting word has no effect, and figuring out why things are not working can be quite a pain
    def is_inflecting_word(self) -> bool:
        vocab = app.col().vocab.with_any_form_in([self.token.base_form, self.token.surface])
        return any(voc for voc in vocab if voc.matching_configuration.bool_flags.is_inflecting_word.is_active)
