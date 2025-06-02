from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from note.note_constants import Tags
from sysutils import ex_sequence
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from typing import Optional

from language_services.janome_ex.word_extraction.location_range import LocationRange
from sysutils.ex_str import newline

_max_lookahead = 12

class TokenTextLocation(Slots):
    __slots__ = ["__weakref__"]

    def __init__(self, analysis: WeakRef[TextAnalysis], token: ProcessedToken, character_start_index: int, token_index: int) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        surface = token.surface
        base = token.base_form
        self.is_shadowed_by: Optional[WeakRef[TokenTextLocation]] = None
        self.token: ProcessedToken = token
        self.analysis: WeakRef[TextAnalysis] = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(surface) - 1
        self.surface: str = surface
        self.base: str = base

        self.word_candidates: list[LocationRange] = []
        self.valid_candidates: list[LocationRange] = []
        self.display_words: list[CandidateWord] = []
        self.all_words: list[CandidateWord] = []
        self.all_candidate_ranges: list[LocationRange] = []
        self.next: Optional[WeakRef[TokenTextLocation]] = None
        self.previous: Optional[WeakRef[TokenTextLocation]] = None

    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.surface} | {self.base})
{newline.join([cand.__repr__() for cand in self.word_candidates])}
"""

    def forward_list(self, length: int = 99999) -> list[TokenTextLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    def analysis_step_1_connect_next_and_previous(self) -> None:
        if len(self.analysis().locations) > self.token_index + 1:
            self.next = WeakRef(self.analysis().locations[self.token_index + 1])

        if self.token_index > 0:
            self.previous = WeakRef(self.analysis().locations[self.token_index - 1])

    def analysis_step_2_analyze_non_compound(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.all_candidate_ranges = [LocationRange([WeakRef(location) for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1)]
        self.all_candidate_ranges[-1].complete_analysis()  # the non-compound part needs to be completed first

    def analysis_step_3_analyze_compounds(self) -> None:
        for range_ in self.all_candidate_ranges[:-1]:  # we already have the last one completed
            range_.complete_analysis()

        self.word_candidates = [candidate for candidate in self.all_candidate_ranges if candidate.is_word]
        self.valid_candidates = [candidate for candidate in self.all_candidate_ranges if candidate.has_valid_words()]
        self.all_words = ex_sequence.flatten([v.all_words for v in self.valid_candidates])

    def analysis_step_4_calculate_preference_between_overlapping_valid_candidates(self) -> None:
        if self.valid_candidates and self.is_shadowed_by is None:
            self.display_words = self.valid_candidates[0].display_words
            self.display_words = [candidate for candidate in self.display_words if not self.is_part_of_other_display_word(candidate)]

            covering_forward_count = self.valid_candidates[0].length - 1
            for location in self.forward_list(covering_forward_count)[1:]:
                location.is_shadowed_by = WeakRef(self)

    def is_part_of_other_display_word(self, word: CandidateWord) -> bool:
        return any(covering for covering in self.display_words if word.form in covering.form and word != covering)

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next().is_inflecting_word()

    # todo: having this check here only means that marking a compound as an inflecting word has no effect, and figuring out why things are not working can be quite a pain
    def is_inflecting_word(self) -> bool:
        vocab = app.col().vocab.with_form(self.base)
        return any(voc for voc in vocab if voc.has_tag(Tags.Vocab.Matching.is_inflecting_word))
