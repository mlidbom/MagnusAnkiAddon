from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import ex_assert

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from typed_linq_collections.collections.q_set import QSet

class TextAnalysisValidator:
    def __init__(self, analysis: TextAnalysis) -> None:
        self.analysis: TextAnalysis = analysis

        self.is_valid_true_matches: QSet[Match] = analysis.all_matches.where(lambda match: match.is_valid).to_set()
        self.is_valid_true_hiding_reasons_empty_matches: QSet[Match] = self.is_valid_true_matches.where(lambda match: len(match.hiding_reasons) == 0).to_set()
        self.is_valid_true_is_displayed_false_matches: QSet[Match] = self.is_valid_true_matches.where(lambda match: not match.is_displayed).to_set()
        self.is_displayed_true_matches: QSet[Match] = analysis.all_matches.where(lambda match: match.is_displayed).to_set()
        self.is_valid_false_matches: QSet[Match] = analysis.all_matches.where(lambda match: not match.is_valid).to_set()
        self.valid_matches: QSet[Match] = analysis.valid_matches.to_set()

    def assert_is_valid(self) -> None:
        self.is_valid_false_matches_should_have_failure_reasons()
        self.is_valid_true_is_displayed_false_matches_should_have_hiding_reasons()
        self.is_valid_true_matches_should_be_in_valid_matches()
        self.is_valid_true_hiding_reasons_empty_matches_should_have_is_displayed_true()
        self.is_valid_true_matches_should_be_in_indexing_matches()
        # self.display_matches_should_be_in_valid_matches()
        # self.is_displayed_true_matches_should_have_is_valid_true()
        # self.is_valid_false_matches_should_not_be_in_indexing_matches()
        # self.is_valid_true_matches_should_be_in_valid_variant_valid_matches()
        # self.valid_matches_and_valid_variant_matches_should_be_identical()


    def is_valid_true_is_displayed_false_matches_should_have_hiding_reasons(self) -> None:
        self.is_valid_true_is_displayed_false_matches.for_each(lambda match: ex_assert.that(len(match.hiding_reasons) > 0, lambda: f"""Match: {match} has is_displayed=False yet has no hiding_reasons"""))

    def is_valid_true_hiding_reasons_empty_matches_should_have_is_displayed_true(self) -> None:
        self.is_valid_true_hiding_reasons_empty_matches.for_each(lambda match: ex_assert.that(match.is_displayed, lambda: f"""Match: {match} has is_valid=True and hiding_reasons=Empty yet has is_displayed=False"""))

    # def is_valid_false_matches_should_not_be_in_indexing_matches(self) -> None:
    #     self.is_valid_false_matches.for_each(lambda match: ex_assert.that(match not in self.analysis.indexing_matches, lambda: f"""Match: {match} has is_valid=False yet is in indexing_matches"""))

    # def is_displayed_true_matches_should_have_is_valid_true(self) -> None:
    #     self.is_displayed_true_matches.for_each(lambda match: ex_assert.that(match.is_valid, lambda: f"""Match: {match} has is_displayed=True yet has is_valid=False"""))

    def is_valid_true_matches_should_be_in_valid_matches(self) -> None:
        self.is_valid_true_matches.for_each(lambda match: ex_assert.that(match in self.valid_matches, lambda: f"""Match: {match} has is_valid=True yet is not in valid_matches"""))

    def is_valid_true_matches_should_be_in_indexing_matches(self) -> None:
        self.is_valid_true_matches.for_each(lambda match: ex_assert.that(match in self.analysis.indexing_matches, lambda: f"""Match: {match} has is_valid=True yet is not in valid_matches"""))

    # def display_matches_should_be_in_valid_matches(self) -> None:
    #     self.display_matches.for_each(lambda match: ex_assert.that(match in self.valid_matches, lambda: f"""Match: {match} ##  is in display matches, yet is not in valid_matches"""))

    def is_valid_false_matches_should_have_failure_reasons(self) -> None:
        self.is_valid_false_matches.for_each(lambda match: ex_assert.that(len(match.failure_reasons) > 0, lambda: f"""Match: {match} has is_valid=False yet has no failure_reasons"""))

#     def is_valid_true_matches_should_be_in_valid_variant_valid_matches(self) -> None:
#         self.is_valid_true_matches.for_each(lambda match: ex_assert.that(match in self.valid_variant_valid_matches, lambda: f"""Match: {match} has is_valid=True yet is not in valid_variant_valid_matches"""))
#
#     def valid_matches_and_valid_variant_matches_should_be_identical(self) -> None:
#         self.valid_matches.for_each(lambda match: ex_assert.that(match in self.valid_variant_valid_matches, lambda: f"""Match: {match} is in valid_matches but not in valid_variant_valid_matches"""))
#         self.valid_variant_valid_matches.for_each(lambda match: ex_assert.that(match in self.valid_matches, lambda: f"""Match: {match} is in valid_variant_valid_matches but not in valid_matches"""))
#
# class WordVariantValidator:
#     def __init__(self, analysis: TextAnalysis) -> None:
#         self.analysis: TextAnalysis = analysis
