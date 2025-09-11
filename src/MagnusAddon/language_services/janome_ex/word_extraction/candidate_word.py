from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.analysis_constants import noise_characters
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
        self.starts_with_non_word_token = self.start_location().token.is_non_word_character

        self.surface_form = "".join([t().token.surface for t in self.locations])
        self.base_form = "".join([location().token.surface for location in self.locations[:-1]]) + self.locations[-1]().token.base_form

        self.surface_variant: CandidateWordSurfaceVariant = CandidateWordSurfaceVariant(self.weakref, self.surface_form)
        self.base_variant: CandidateWordBaseVariant | None = CandidateWordBaseVariant(self.weakref, self.base_form) if self.base_form != self.surface_form else None

        self.is_word: bool = self.surface_variant.is_known_word or self.base_variant is not None and self.base_variant.is_known_word

        self.is_inflectable_word: bool = self.end_location().token.is_inflectable_word
        self.next_token_is_inflecting_word: bool = self.end_location().is_next_location_inflecting_word()
        self.is_inflected_word: bool = self.is_inflectable_word and self.next_token_is_inflecting_word

        self.starts_with_non_word_character: bool = self.starts_with_non_word_token or self.surface_form in noise_characters

        self.should_include_surface_in_all_words: bool = False
        self.should_include_base_in_valid_words: bool = False
        self.should_include_base_in_display_variants: bool = False
        self.should_include_surface_in_display_variants: bool = False
        self.should_include_surface_in_valid_words: bool = False
        self.all_word_variants: list[CandidateWordVariant] = []
        self.valid_variants: list[CandidateWordVariant] = []
        self.display_word_variants: list[CandidateWordVariant] = []

    def has_seemingly_valid_single_token(self) -> bool:
        return not self.is_custom_compound and not self.starts_with_non_word_character

    def run_validity_analysis(self) -> None:
        self.surface_variant.complete_analysis()
        if self.base_variant is not None: self.base_variant.complete_analysis()

        self.should_include_base_in_valid_words = self.base_variant is not None and self.base_variant.is_valid_candidate

        self.should_include_surface_in_valid_words = (self.surface_variant.is_valid_candidate
                                                      and (self.base_variant is None or self.surface_variant.form != self.base_variant.form)
                                                      and (not self.is_inflected_word or not self.should_include_base_in_valid_words))

        self.should_include_surface_in_all_words = (self.should_include_surface_in_valid_words
                                                    or (not self.should_include_base_in_valid_words and self.has_seemingly_valid_single_token()))

        self.valid_variants = []
        if self.base_variant is not None and self.should_include_base_in_valid_words:
            self.valid_variants.append(self.base_variant)
        if self.should_include_surface_in_valid_words:
            self.valid_variants.append(self.surface_variant)

        if self.surface_variant.is_known_word or self.should_include_surface_in_all_words:
            self.all_word_variants.append(self.surface_variant)

        if self.base_variant is not None and (self.base_variant.is_known_word or self.should_include_base_in_valid_words):
            self.all_word_variants.append(self.base_variant)

    def run_display_analysis_pass_true_if_there_were_changes(self) -> bool:
        old_display_word_variants = self.display_word_variants
        self.display_word_variants = []
        self.should_include_base_in_display_variants = (self.base_variant is not None
                                                        and self.should_include_base_in_valid_words
                                                        and any(self.base_variant.display_matches))

        self.should_include_surface_in_display_variants = (self.should_include_surface_in_all_words and any(self.surface_variant.display_matches))

        if self.should_include_surface_in_display_variants:
            self.display_word_variants.append(self.surface_variant)
        elif self.should_include_base_in_display_variants:
            self.display_word_variants.append(non_optional(self.base_variant))

        if len(old_display_word_variants) != len(self.display_word_variants):
            return True

        return any(old_display_word_variants[index] != self.display_word_variants[index] for index in range(len(old_display_word_variants)))

    def has_valid_words(self) -> bool: return len(self.valid_variants) > 0

    def __repr__(self) -> str: return f"""
surface: {self.surface_variant.__repr__()} | base:{self.base_variant.__repr__()},
hdc:{self.has_valid_words()},
iw:{self.is_word}
icc:{self.is_custom_compound})""".replace(newline, "")
