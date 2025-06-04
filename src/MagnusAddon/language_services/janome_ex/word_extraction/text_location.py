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
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.match import Match
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

from typing import Optional

from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
from sysutils.ex_str import newline

_max_lookahead = 12

class TextAnalysisLocation(Slots):
    __slots__ = ["__weakref__"]

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

    def analysis_step_1_analyze_non_compound(self) -> None:
        lookahead_max = min(_max_lookahead, len(self.forward_list(_max_lookahead)))
        self.all_candidate_ranges = [CandidateWord([location.weakref for location in self.forward_list(index)]) for index in range(lookahead_max - 1, -1, -1)]
        self.all_candidate_ranges[-1].complete_analysis()  # the non-compound part needs to be completed first

    def analysis_step_2_analyze_compounds(self) -> None:
        for range_ in self.all_candidate_ranges[:-1]:  # we already have the last one completed
            range_.complete_analysis()

    def analysis_step_3_create_collections(self) -> None:
        self.candidate_words_starting_here = [candidate for candidate in self.all_candidate_ranges if candidate.is_word]
        self.valid_words_starting_here = [candidate for candidate in self.all_candidate_ranges if candidate.has_valid_words()]
        self.display_words_starting_here = [candidate for candidate in self.all_candidate_ranges if candidate.has_display_words()]
        self.valid_variants = ex_sequence.flatten([v.valid_variants for v in self.valid_words_starting_here])
        self.all_word_variants = ex_sequence.flatten([v.all_word_variants for v in self.all_candidate_ranges])

    def analysis_step_4_calculate_preference_between_overlapping_display_variants(self) -> None:
        #todo this does not belong here. The cand should never have display words that are not displayed in the first place.
        def candidate_has_display_matches(cand: CandidateWord) -> bool:
            matches:list[Match] = ex_sequence.flatten([variant.matches for variant in cand.display_word_variants])
            if any(match for match in matches if match.is_displayed):
                return True
            return False

        while self.display_words_starting_here and not candidate_has_display_matches(self.display_words_starting_here[0]):
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
