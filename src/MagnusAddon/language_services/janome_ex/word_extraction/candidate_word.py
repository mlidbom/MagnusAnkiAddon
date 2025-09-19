from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from ex_autoslot import AutoSlots
from language_services.janome_ex.word_extraction.analysis_constants import noise_characters
from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
from language_services.janome_ex.word_extraction.matches.match import Match
from sysutils.collections.queryable.q_iterable import QIterable
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from sysutils.collections.queryable.q_list import QList

from sysutils.ex_str import newline


@final
class CandidateWord(WeakRefable, AutoSlots):
    def __init__(self, locations: list[WeakRef[TextAnalysisLocation]]) -> None:
        self.weakref = WeakRef(self)
        self.locations: list[WeakRef[TextAnalysisLocation]] = locations

        self.surface_form = "".join([t().token.surface for t in self.locations])
        self.base_form = "".join([location().token.surface for location in self.locations[:-1]]) + self.locations[-1]().token.base_form
        self.surface_variant: CandidateWordVariant = CandidateWordVariant(self.weakref, self.surface_form)
        self.base_variant: CandidateWordVariant | None = CandidateWordVariant(self.weakref, self.base_form) if self.base_form != self.surface_form else None

        self.indexing_variants: list[CandidateWordVariant] = []
        self.valid_variants: list[CandidateWordVariant] = []
        self.display_variants: list[CandidateWordVariant] = []

    @property
    def should_include_surface_in_valid_words(self) -> bool: return (self.surface_variant.is_valid
                                                                     and (not self.is_inflected_word or not self.has_valid_base_variant))
    @property
    def has_valid_base_variant(self) -> bool: return self.base_variant is not None and self.base_variant.is_valid
    @property
    def should_include_surface_in_all_words(self) -> bool: return (self.should_include_surface_in_valid_words
                                                                   or (not self.has_valid_base_variant and self.has_seemingly_valid_single_token))
    @property
    def has_valid_base_with_display_matches(self) -> bool: return self.has_valid_base_variant and any(non_optional(self.base_variant).display_matches)
    @property
    def should_include_surface_in_display_variants(self) -> bool: return self.should_include_surface_in_all_words and any(self.surface_variant.display_matches)
    @property
    def should_index_base(self) -> bool: return self.base_variant is not None and (self.base_variant.is_known_word or self.has_valid_base_variant)
    @property
    def should_index_surface(self) -> bool: return self.surface_variant.is_known_word or self.should_include_surface_in_all_words


    @property
    def all_matches(self) -> QList[Match]:
        return self.surface_variant.matches.concat(self.base_variant.matches if self.base_variant else QIterable[Match].empty()).to_list()

    def run_validity_analysis(self) -> None:
        self.surface_variant.run_validity_analysis()
        if self.base_variant is not None: self.base_variant.run_validity_analysis()

        self.valid_variants = []
        if self.has_valid_base_variant:
            self.valid_variants.append(non_optional(self.base_variant))
        if self.should_include_surface_in_valid_words:
            self.valid_variants.append(self.surface_variant)

        if self.should_index_surface:
            self.indexing_variants.append(self.surface_variant)

        if self.should_index_base:
            self.indexing_variants.append(non_optional(self.base_variant))

    def run_display_analysis_pass_true_if_there_were_changes(self) -> bool:
        old_display_word_variants = self.display_variants
        self.display_variants = []

        if self.should_include_surface_in_display_variants:
            self.display_variants.append(self.surface_variant)
        elif self.has_valid_base_with_display_matches:
            self.display_variants.append(non_optional(self.base_variant))

        def displaywords_were_changed() -> bool:
            if len(old_display_word_variants) != len(self.display_variants):
                return True

            return any(old_display_word_variants[index] != self.display_variants[index] for index in range(len(old_display_word_variants)))

        return displaywords_were_changed()

    def has_valid_words(self) -> bool: return len(self.valid_variants) > 0

    @property
    def has_seemingly_valid_single_token(self) -> bool: return not self.is_custom_compound and not self.starts_with_non_word_character
    @property
    def analysis(self) -> TextAnalysis: return self.locations[0]().analysis()
    @property
    def is_custom_compound(self) -> bool: return self.location_count > 1
    @property
    def start_location(self) -> TextAnalysisLocation: return self.locations[0]()
    @property
    def end_location(self) -> TextAnalysisLocation: return self.locations[-1]()
    @property
    def location_count(self) -> int: return len(self.locations)
    @property
    def starts_with_non_word_token(self) -> bool: return self.start_location.token.is_non_word_character

    @property
    def is_word(self) -> bool: return self.surface_variant.is_known_word or (self.base_variant is not None and self.base_variant.is_known_word)
    @property
    def is_inflectable_word(self) -> bool: return self.end_location.token.is_inflectable_word
    @property
    def next_token_is_inflecting_word(self) -> bool: return self.end_location.is_next_location_inflecting_word()
    @property
    def is_inflected_word(self) -> bool: return self.is_inflectable_word and self.next_token_is_inflecting_word
    @property
    def starts_with_non_word_character(self) -> bool: return self.starts_with_non_word_token or self.surface_form in noise_characters

    @property
    def is_shadowed(self) -> bool: return self.is_shadowed_by is not None
    @property
    def shadowed_by_text(self) -> str: return non_optional(self.is_shadowed_by).form if self.is_shadowed else ""
    @property
    def is_shadowed_by(self) -> CandidateWordVariant | None:
        if any(self.start_location.is_shadowed_by):
            return self.start_location.is_shadowed_by[0]().display_variants[0]
        if (any(self.start_location.display_variants)
                and self.start_location.display_variants[0].word.location_count > self.location_count):
            return self.start_location.display_variants[0]
        return None

    @override
    def __repr__(self) -> str: return f"""
surface: {self.surface_variant.__repr__()} | base:{self.base_variant.__repr__()},
hdc:{self.has_valid_words()},
iw:{self.is_word}
icc:{self.is_custom_compound})""".replace(newline, "")
