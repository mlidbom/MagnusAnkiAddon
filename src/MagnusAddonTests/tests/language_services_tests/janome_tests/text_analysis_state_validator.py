from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from sysutils.collections.linq.q_iterable import QSet

class TextAnalysisStateValidator:
    def __init__(self, analysis: TextAnalysis) -> None:
        self.analysis = analysis

        self.is_valid_true_matches:QSet[Match] = analysis.all_matches.where(lambda match: match.is_valid).to_set()
        self.is_valid_true_is_displayed_false_matches:QSet[Match] = self.is_valid_true_matches.where(lambda match: not match.is_displayed).to_set()
        self.is_displayed_true_matches:QSet[Match] = analysis.all_matches.where(lambda match: match.is_displayed).to_set()
        self.is_valid_false_matches:QSet[Match] = analysis.all_matches.where(lambda match: not match.is_valid).to_set()
        self.display_matches:QSet[Match] = analysis.display_matches.to_set()

    def assert_is_valid(self) -> None:
        print(self.analysis.text)
        self.is_displayed_false_matches_should_not_be_in_displayed_matches_list()
        self.is_displayed_true_matches_should_be_in_display_matches()
        self.is_valid_false_matches_should_have_failure_reasons()
        self.is_valid_true_is_displayed_false_matches_should_have_hiding_reasons()

    def is_displayed_false_matches_should_not_be_in_displayed_matches_list(self) -> None:
        self.is_valid_true_is_displayed_false_matches.assert_each(lambda match: match not in self.display_matches, lambda match: f"""Match: {match} has is_displayed=False yet is displayed""")

    def is_displayed_true_matches_should_be_in_display_matches(self) -> None:
        self.is_displayed_true_matches.assert_each(lambda match: match in self.display_matches, lambda match: f"""Match: {match} has is_displayed=True yet is not in display_matches""")

    def is_valid_true_is_displayed_false_matches_should_have_hiding_reasons(self) -> None:
        self.is_valid_true_is_displayed_false_matches.assert_each(lambda match: len(match.hiding_reasons) > 0, lambda match: f"""Match: {match} has is_displayed=False yet has no hiding_reasons""")

    def is_valid_false_matches_should_have_failure_reasons(self) -> None:
        self.is_valid_false_matches.assert_each(lambda match: len(match.failure_reasons) > 0, lambda match: f"""Match: {match} has is_valid=False yet has no failure_reasons""")
