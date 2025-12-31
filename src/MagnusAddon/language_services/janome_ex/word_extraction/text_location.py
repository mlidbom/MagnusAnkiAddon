from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.processed_token import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.match import Match
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
        self.is_shadowed_by: list[WeakRef[TextAnalysisLocation]] = []
        self.shadows: list[WeakRef[TextAnalysisLocation]] = []
        self.analysis: WeakRef[TextAnalysis] = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(self.token.surface) - 1

        self.display_variants: list[CandidateWordVariant] = []
        self.indexing_variants: QList[CandidateWordVariant] = QList()
        self._candidate_words: QList[CandidateWord] = QList()
        self.compound_matches_extending_past_this_location: QList[Match] = QList()
        self.compound_matches_covering_this_location: QList[Match] = QList()
        self.unyielding_compound_matches_covering_this_location: QList[Match] = QList()

    @override
    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.token.surface} | {self.token.base_form})
{newline.join([cand.__repr__() for cand in self.indexing_variants])}
"""

    def forward_list(self, length: int = 99999) -> list[TextAnalysisLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    def analysis_step_1_analyze_non_compound_validity(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self._candidate_words = QList(CandidateWord([location.weakref for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1))
        self._candidate_words[-1].run_validity_analysis()  # the non-compound part needs to be completed first

    def analysis_step_2_analyze_compound_validity(self) -> None:
        for candidate_word in self._candidate_words[:-1]:  # we already have the last one completed
            candidate_word.run_validity_analysis()

        self.indexing_variants = self._candidate_words.select_many(lambda candidate: candidate.indexing_variants).to_list()
        valid_words = self._candidate_words.where(lambda candidate: candidate.has_valid_words()).to_list()

        for valid_word in valid_words:
            for variant in valid_word.valid_variants:
                for match in variant.valid_matches.where(lambda it: it.is_preliminarily_valid_for_display):
                    for overlapped_location in valid_word.locations[:-1]:
                        overlapped_location().compound_matches_extending_past_this_location.append(match)
                    for covered_location in valid_word.locations[1:]:
                        covered_location().compound_matches_covering_this_location.append(match)
                        if not match.would_yield_to_upcoming_overlapping_compound:
                            covered_location().unyielding_compound_matches_covering_this_location.append(match)

    def analysis_step_3_display_analysis(self) -> None:
        for candidate_word in self._candidate_words:
            candidate_word.run_display_analysis()

        display_words = self._candidate_words.where(lambda it: it.display_variants.any()).to_list()
        self.display_variants = display_words[0].display_variants if display_words.any() else []

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next().is_inflecting_word()

    # todo: having this check here only means that marking a compound as an inflecting word has no effect, and figuring out why things are not working can be quite a pain
    def is_inflecting_word(self) -> bool:
        vocab = app.col().vocab.with_any_form_in([self.token.base_form, self.token.surface])
        return any(voc for voc in vocab if voc.matching_configuration.bool_flags.is_inflecting_word.is_active)
