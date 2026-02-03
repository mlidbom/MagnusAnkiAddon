from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from jaspythonutils.sysutils.weak_ref import WeakRef, WeakRefable

from jaslib import app

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken
    from jaslib.language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from jaslib.language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from jaspythonutils.sysutils.ex_str import newline

from jaslib.language_services.janome_ex.word_extraction.candidate_word import CandidateWord

_max_lookahead = 12  # In my collection the longest so far is 9, so 12 seems a pretty good choice.

@final
class TextAnalysisLocation(WeakRefable, Slots):
    def __init__(self, analysis: WeakRef[TextAnalysis], token: IAnalysisToken, character_start_index: int, token_index: int) -> None:
        self.weakref = WeakRef(self)
        self.next: WeakRef[TextAnalysisLocation] | None = None
        self.previous: WeakRef[TextAnalysisLocation] | None = None
        self.token: IAnalysisToken = token
        self.is_shadowed_by: list[WeakRef[TextAnalysisLocation]] = []
        self.shadows: list[WeakRef[TextAnalysisLocation]] = []
        self.analysis: WeakRef[TextAnalysis] = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(self.token.surface) - 1

        self.display_variants: list[CandidateWordVariant] = []
        self.indexing_variants: list[CandidateWordVariant] = []
        self.candidate_words: list[CandidateWord] = []
        self.display_words: list[CandidateWord] = []

    @override
    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.token.surface} | {self.token.base_form})
{newline.join([cand.__repr__() for cand in self.indexing_variants])}
"""

    def forward_list(self, length: int = 99999) -> list[TextAnalysisLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    @property
    def non_compound_candidate(self) -> CandidateWord: return self.candidate_words[-1]

    def analysis_step_1_analyze_non_compound_validity(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.candidate_words = [CandidateWord([location.weakref for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1)]
        self.candidate_words[-1].run_validity_analysis()  # the non-compound part needs to be completed first

    def analysis_step_2_analyze_compound_validity(self) -> None:
        for range_ in self.candidate_words[:-1]:  # we already have the last one completed
            range_.run_validity_analysis()

        self.indexing_variants = [variant for cand in self.candidate_words for variant in cand.indexing_variants]

    def run_display_analysis_and_update_display_words_pass_true_if_there_were_changes(self) -> bool:
        changes_made = False
        for range_ in self.candidate_words:
            if range_.run_display_analysis_pass_true_if_there_were_changes():
                changes_made = True

        if changes_made:
            self.display_words = [it for it in self.candidate_words if it.display_variants]
        return changes_made

    def analysis_step_3_run_display_analysis_without_shadowing_information_so_that_all_valid_matches_are_displayed_and_can_be_accounted_for_in_yielding_to_upcoming_compounds(self) -> None:
        self.run_display_analysis_and_update_display_words_pass_true_if_there_were_changes()

    def analysis_step_4_set_initial_shadowing_and_recalculate_display_words_return_true_on_changes(self) -> bool:
        display_words_updated = self.run_display_analysis_and_update_display_words_pass_true_if_there_were_changes()
        self.update_shadowing()
        return display_words_updated

    def analysis_step_5_update_shadowing_and_recalculate_display_words_return_true_on_changes(self) -> bool:
        display_words_updated = self.run_display_analysis_and_update_display_words_pass_true_if_there_were_changes()
        if display_words_updated:
            self.update_shadowing()
        return display_words_updated

    def update_shadowing(self) -> None:
        if self.display_words and not self.display_words[0].is_shadowed:
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
