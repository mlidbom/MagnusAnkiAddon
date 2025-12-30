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

_max_lookahead = 12 # In my collection the longest so far is 9, so 12 seems a pretty good choice.

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

        self.known_words: list[CandidateWord] = []
        self.valid_words: QList[CandidateWord] = QList()
        self.display_variants: list[CandidateWordVariant] = []
        self.valid_variants: QList[CandidateWordVariant] = QList()
        self.indexing_variants: QList[CandidateWordVariant] = QList()
        self.candidate_words: QList[CandidateWord] = QList()
        self.display_words: list[CandidateWord] = []
        # Valid compounds that overlap this location and extend beyond it.
        # A match ending at this location might yield to one of these if it has yield_last_token.
        # Pre-computed for efficient lookup by HasDisplayedOverlappingFollowingCompound.
        self.yield_target_candidates: list[CandidateWord] = []
        # Valid, non-hidden matches that start BEFORE this location and extend OVER it.
        # Used by IsShadowed to check if this location is shadowed by an earlier match.
        self.covering_matches: list[Match] = []

    @override
    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.token.surface} | {self.token.base_form})
{newline.join([cand.__repr__() for cand in self.known_words])}
"""

    def forward_list(self, length: int = 99999) -> list[TextAnalysisLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    def analysis_step_1_analyze_non_compound_validity(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.candidate_words = QList(CandidateWord([location.weakref for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1))
        self.candidate_words[-1].run_validity_analysis()  # the non-compound part needs to be completed first

    def analysis_step_2_analyze_compound_validity(self) -> None:
        for range_ in self.candidate_words[:-1]:  # we already have the last one completed
            range_.run_validity_analysis()

        self.known_words = self.candidate_words.where(lambda candidate: candidate.is_word).to_list()
        self.valid_words = self.candidate_words.where(lambda candidate: candidate.has_valid_words()).to_list()
        self.indexing_variants = self.candidate_words.select_many(lambda candidate: candidate.indexing_variants).to_list()
        self.valid_variants = self.valid_words.select_many(lambda valid: valid.valid_variants).to_list()

        # Register each valid compound as a potential yield target at each location it overlaps.
        # A compound at [start, end] is a yield target candidate for locations start..end-1
        # (i.e., locations where it overlaps AND extends beyond).
        for valid_word in self.valid_words:
            for overlapped_location in valid_word.locations[:-1]:  # All locations except the last
                overlapped_location().yield_target_candidates.append(valid_word)

        # Register each valid, non-hidden match as covering each location in its word's interior.
        # A word at [start, end] covers locations start+1..end-1.
        from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_hidden import IsConfiguredHidden
        for valid_word in self.valid_words:
            for variant in valid_word.valid_variants:
                for match in variant.matches:
                    if not match.is_valid:
                        continue
                    if IsConfiguredHidden(match.weakref).match_is_in_state:
                        continue
                    # Register this match as covering interior locations
                    for covered_location in valid_word.locations[1:-1]:
                        covered_location().covering_matches.append(match)

    def _run_display_analysis_pass_true_if_there_were_changes(self) -> bool:
        changes_made = False
        for range_ in self.candidate_words:
            if range_.run_display_analysis_pass_true_if_there_were_changes():
                changes_made = True

        if changes_made:
            self.display_words = [candidate for candidate in self.candidate_words if candidate.display_variants]
        return changes_made

    def run_display_analysis_and_update_display_words(self) -> bool:
        """Re-evaluate display status of all candidate words at this location.

        This method checks each candidate word's matches for display eligibility,
        which includes checking HasDisplayedOverlappingFollowingCompound (for words
        marked with yield_last_token). When called right-to-left, the display_words
        at forward locations are already resolved, so yield decisions are accurate.

        Returns True if any changes were made to display_variants.
        """
        return self._run_display_analysis_pass_true_if_there_were_changes()

    def resolve_shadowing_for_display_word(self) -> None:
        """Set up shadowing relationships based on the first display word at this location.

        If this location has display_words and isn't already shadowed by a longer word:
        - Set this location's display_variants to the first display word's variants
        - Mark all forward locations within the display word's range as shadowed

        This method should be called left-to-right after yield resolution, so that
        longer words at earlier positions can shadow shorter/later words.
        """
        if self.display_words and not any(self.is_shadowed_by):
            self.display_variants = self.display_words[0].display_variants

            covering_forward_count = self.display_words[0].location_count - 1
            for shadowed in self.forward_list(covering_forward_count)[1:]:
                shadowed.is_shadowed_by.append(self.weakref)
                self.shadows.append(shadowed.weakref)
                # If the shadowed location was shadowing others, clear that
                for shadowed_shadowed in shadowed.shadows:
                    shadowed_shadowed().is_shadowed_by.remove(shadowed.weakref)
                shadowed.shadows.clear()

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next().is_inflecting_word()

    # todo: having this check here only means that marking a compound as an inflecting word has no effect, and figuring out why things are not working can be quite a pain
    def is_inflecting_word(self) -> bool:
        vocab = app.col().vocab.with_any_form_in([self.token.base_form, self.token.surface])
        return any(voc for voc in vocab if voc.matching_configuration.bool_flags.is_inflecting_word.is_active)
