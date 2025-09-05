from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordBaseVariant, CandidateWordSurfaceVariant, CandidateWordVariant
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation

from sysutils.ex_str import newline


class CandidateWord(WeakRefable, Slots):
    def __init__(self, locations: list[WeakRef[TextAnalysisLocation]]) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.analysis: WeakRef[TextAnalysis] = locations[0]().analysis
        self.locations: list[WeakRef[TextAnalysisLocation]] = locations
        self.is_custom_compound: bool = len(locations) > 1
        self.start_location: WeakRef[TextAnalysisLocation] = self.locations[0]
        self.end_location: WeakRef[TextAnalysisLocation] = self.locations[-1]
        self.location_count = len(self.locations)
        self.weakref = WeakRef(self)

        surface_form = "".join([t().token.surface for t in self.locations])

        base_form = "".join([location().token.surface for location in self.locations[:-1]]) + self.locations[-1]().token.base_form
        if not self.is_custom_compound:
            base_form = self.locations[0]().token.base_form_for_non_compound_vocab_matching

        self.surface: CandidateWordSurfaceVariant = CandidateWordSurfaceVariant(self.weakref, surface_form)
        self.base: CandidateWordBaseVariant | None = CandidateWordBaseVariant(self.weakref, base_form) if base_form != surface_form else None

        self.is_word: bool = self.surface.is_word or self.base is not None and self.base.is_word

        self.is_inflectable_word: bool = self.end_location().token.is_inflectable_word
        self.next_token_is_inflecting_word: bool = self.end_location().is_next_location_inflecting_word()
        self.is_inflected_word: bool = self.is_inflectable_word and self.next_token_is_inflecting_word

        self.should_include_surface_in_all_words: bool = False
        self.should_include_base_in_valid_words: bool = False
        self.should_include_base_in_display_variants: bool = False
        self.should_include_surface_in_display_variants: bool = False
        self.should_include_surface_in_valid_words: bool = False
        self.all_word_variants: list[CandidateWordVariant] = []
        self.valid_variants: list[CandidateWordVariant] = []
        self.display_word_variants: list[CandidateWordVariant] = []

    def must_include_some_variant(self) -> bool:
        return (not self.is_custom_compound
                and not self.surface.starts_with_non_word_token
                and not self.surface.is_noise_character)

    def run_validity_analysis(self) -> None:
        self.surface.complete_analysis()
        if self.base is not None: self.base.complete_analysis()

        self.should_include_base_in_valid_words = self.base is not None and self.base.is_valid_candidate

        self.should_include_surface_in_valid_words = (self.surface.is_valid_candidate
                                                      and (self.base is None or self.surface.form != self.base.form)
                                                      and (not self.is_inflected_word or not self.should_include_base_in_valid_words))

        self.should_include_surface_in_all_words = (self.should_include_surface_in_valid_words
                                                    or (not self.should_include_base_in_valid_words and self.must_include_some_variant()))

        self.valid_variants = []
        if self.base is not None and self.should_include_base_in_valid_words:
            self.valid_variants.append(self.base)
        if self.should_include_surface_in_valid_words:
            self.valid_variants.append(self.surface)

        if self.surface.is_word or self.should_include_surface_in_all_words:
            self.all_word_variants.append(self.surface)

        if self.base is not None and (self.base.is_word or self.should_include_base_in_valid_words):
            self.all_word_variants.append(self.base)

    def run_display_analysis(self) -> None:
        self.should_include_base_in_display_variants = (self.base is not None
                                                        and self.should_include_base_in_valid_words
                                                        and any(self.base.display_matches))

        self.should_include_surface_in_display_variants = (self.should_include_surface_in_all_words and any(self.surface.display_matches))

        if self.should_include_surface_in_display_variants:
            self.display_word_variants.append(self.surface)
        elif self.should_include_base_in_display_variants:
            self.display_word_variants.append(non_optional(self.base))

    def has_valid_words(self) -> bool: return len(self.valid_variants) > 0
    # todo strange order dependency makes the first collection potentially invalid later. Ugh
    def display_words_are_still_valid(self) -> bool: return (len(self.display_word_variants) > 0
                                                             and any(any(variant.display_matches) for variant in self.display_word_variants))

    def __repr__(self) -> str: return f"""
surface: {self.surface.__repr__()} | base:{self.base.__repr__()},
hdc:{self.has_valid_words()},
iw:{self.is_word}
icc:{self.is_custom_compound})""".replace(newline, "")
