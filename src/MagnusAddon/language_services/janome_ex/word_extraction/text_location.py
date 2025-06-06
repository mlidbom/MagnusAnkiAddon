from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from note.note_constants import Tags
from sysutils import ex_sequence
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from typing import Optional

from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_max_lookahead = 12

class TextAnalysisLocation(WeakRefable,Slots):
    def __init__(self, analysis: WeakRef[TextAnalysis], token: ProcessedToken, character_start_index: int, token_index: int) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.weakref = WeakRef(self)
        self.next: Optional[WeakRef[TextAnalysisLocation]] = None
        self.previous: Optional[WeakRef[TextAnalysisLocation]] = None
        self.token: ProcessedToken = token
        self.is_shadowed_by: Optional[WeakRef[TextAnalysisLocation]] = None
        self.analysis: WeakRef[TextAnalysis] = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(self.token.surface) - 1

        self.candidate_words_starting_here: list[CandidateWord] = []
        self.valid_words_starting_here: list[CandidateWord] = []
        self.display_variants: list[CandidateWordVariant] = []
        self.valid_variants: list[CandidateWordVariant] = []
        self.all_word_variants: list[CandidateWordVariant] = []
        self.all_candidate_ranges: list[CandidateWord] = []
        self.display_words_starting_here: list[CandidateWord] = []

    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.token.surface} | {self.token.base_form})
{newline.join([cand.__repr__() for cand in self.candidate_words_starting_here])}
"""

    def forward_list(self, length: int = 99999) -> list[TextAnalysisLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    def analysis_step_1_analyze_non_compound_validity(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.all_candidate_ranges = [CandidateWord([location.weakref for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1)]
        self.all_candidate_ranges[-1].run_validity_analysis()  # the non-compound part needs to be completed first

    def analysis_step_2_analyze_compound_validity(self) -> None:
        for range_ in self.all_candidate_ranges[:-1]:  # we already have the last one completed
            range_.run_validity_analysis()

    def analysis_step_3_analyze_display_status(self) -> None:
        for range_ in self.all_candidate_ranges:
            range_.run_display_analysis()

    def analysis_step_4_create_collections(self) -> None:
        self.candidate_words_starting_here = [candidate for candidate in self.all_candidate_ranges if candidate.is_word]
        self.valid_words_starting_here = [candidate for candidate in self.all_candidate_ranges if candidate.has_valid_words()]
        self.display_words_starting_here = [candidate for candidate in self.all_candidate_ranges if candidate.display_words_are_still_valid()]
        self.valid_variants = ex_sequence.flatten([word.valid_variants for word in self.valid_words_starting_here])
        self.all_word_variants = ex_sequence.flatten([v.all_word_variants for v in self.all_candidate_ranges])

    def analysis_step_5_calculate_preference_between_overlapping_display_variant5(self) -> None:
        #todo this does not feel great. Currently we need the first version of display_words_starting_here to be created
        # in order for the DisplayRequirements class to inspect it and mark itself as not being displayed so that it can be removed here.
        # this is some truly strange invisible order dependency that is making me quite incomfortable
        # it also relies on the check for is_yield_last_token_to_overlapping_compound_requirement_fulfilled to return different values at different times
        while self.display_words_starting_here and not self.display_words_starting_here[0].display_words_are_still_valid():
            self.display_words_starting_here.remove(self.display_words_starting_here[0])

        if self.display_words_starting_here and self.is_shadowed_by is None:
            self.display_variants = self.display_words_starting_here[0].display_word_variants

            covering_forward_count = self.display_words_starting_here[0].location_count - 1
            for location in self.forward_list(covering_forward_count)[1:]:
                location.is_shadowed_by = self.weakref

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next().is_inflecting_word()

    # todo: having this check here only means that marking a compound as an inflecting word has no effect, and figuring out why things are not working can be quite a pain
    def is_inflecting_word(self) -> bool:
        vocab = app.col().vocab.with_any_form_in([self.token.base_form, self.token.surface])
        return any(voc for voc in vocab if voc.has_tag(Tags.Vocab.Matching.is_inflecting_word))
