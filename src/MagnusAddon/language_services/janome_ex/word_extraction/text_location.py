from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from note.note_constants import Mine
from sysutils import ex_sequence
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_tokenized_text import ProcessedToken
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from typing import Optional

from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_max_lookahead = 12

class TokenTextLocation(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, analysis: WeakRef[TextAnalysis], token: ProcessedToken, character_start_index: int, token_index: int) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        surface = token.surface
        base = token.base_form
        self.is_covered_by: Optional[WeakRef[TokenTextLocation]] = None
        self.token: ProcessedToken = token
        self.analysis: WeakRef[TextAnalysis] = analysis
        self.token_index: int = token_index
        self.character_start_index: int = character_start_index
        self.character_end_index: int = character_start_index + len(surface) - 1
        self.surface: str = surface
        self.base: str = base

        self.word_candidates: list[CandidateWord] = []
        self.valid_candidates: list[CandidateWord] = []
        self.display_words: list[CandidateForm] = []
        self.all_words: list[CandidateForm] = []
        self.all_candidates: list[CandidateWord] = []
        self.next: Optional[WeakRef[TokenTextLocation]] = None
        self.previous: Optional[WeakRef[TokenTextLocation]] = None

    def __repr__(self) -> str:
        return f"""
TextLocation('{self.character_start_index}-{self.character_end_index}, {self.surface} | {self.base})
{newline.join([cand.__repr__() for cand in self.word_candidates])}
"""

    def forward_list(self, length: int = 99999) -> list[TokenTextLocation]:
        return self.analysis().locations[self.token_index: self.token_index + length + 1]

    def run_analysis_step_1(self) -> None:
        if len(self.analysis().locations) > self.token_index + 1:
            self.next = WeakRef(self.analysis().locations[self.token_index + 1])

        if self.token_index > 0:
            self.previous = WeakRef(self.analysis().locations[self.token_index - 1])

        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.all_candidates = [CandidateWord([WeakRef(location) for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1)]
        self.all_candidates[-1].complete_analysis()  # the non-compound part needs to be completed first

    def run_analysis_step_2(self) -> None:
        for cand in self.all_candidates[:-1]:  # we already have the last one completed
            cand.complete_analysis()

        self.word_candidates = [word for word in self.all_candidates if word.is_word]
        self.valid_candidates = [word for word in self.all_candidates if word.has_valid_candidates()]

        if self.valid_candidates and self.is_covered_by is None:
            self.display_words = self.valid_candidates[0].display_words
            self.display_words = [covered for covered in self.display_words
                                  if not any(covering for covering in self.display_words if covered.form in covering.form and covered != covering)]

            covering_forward_count = self.valid_candidates[0].length - 1
            for location in self.forward_list(covering_forward_count)[1:]:
                location.is_covered_by = WeakRef(self)

        self.all_words = ex_sequence.flatten([v.all_words for v in self.valid_candidates])

    def is_next_location_inflecting_word(self) -> bool:
        return self.next is not None and self.next().is_inflecting_word()

    def is_inflecting_word(self) -> bool:
        vocab = app.col().vocab.with_form(self.base)
        return any(voc for voc in vocab if voc.has_tag(Mine.Tags.inflecting_word))
