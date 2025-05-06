from __future__ import annotations
from typing import TYPE_CHECKING
from language_services.janome_ex.word_extraction.candidate_form import BaseCandidateForm, CandidateForm, SurfaceCandidateForm

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.text_location import TokenTextLocation

from sysutils.ex_str import newline

class CandidateWord:
    def __init__(self, locations: list[TokenTextLocation]):
        self.analysis: TextAnalysis = locations[0].analysis
        self.locations: list[TokenTextLocation] = locations
        self.is_custom_compound: bool = len(locations) > 1
        self.start_location: TokenTextLocation = self.locations[0]
        self.end_location: TokenTextLocation = self.locations[-1]
        self.length = len(self.locations)

        self.surface: SurfaceCandidateForm = SurfaceCandidateForm(self)
        self.base: CandidateForm = BaseCandidateForm(self)

        self.is_word: bool = self.surface.is_word or self.base.is_word

        self.is_inflectable_word: bool = self.end_location.token.is_inflectable_word
        self.next_token_is_inflecting_word: bool = self.end_location.is_next_location_inflecting_word()
        self.is_inflected_word: bool = self.is_inflectable_word and self.next_token_is_inflecting_word

        self.should_include_surface: bool = False
        self.should_include_base: bool = False
        self.display_words: list[CandidateForm] = []

    def complete_analysis(self) -> None:
        self.base.complete_analysis()
        self.surface.complete_analysis()

        self.should_include_surface = (self.surface.is_valid_candidate()
                                       and not self.is_inflected_word
                                       and self.surface.form != self.base.form
                                       and self.surface.form not in self.base.forms_excluded_by_vocab_configuration)
        self.should_include_base = (self.base.is_valid_candidate()
                                    and self.base.form not in self.surface.forms_excluded_by_vocab_configuration)

        self.display_words = []
        if self.should_include_base:
            self.display_words.append(self.base)
        if self.should_include_surface:
            self.display_words.append(self.surface)

    def has_valid_candidates(self) -> bool: return len(self.display_words) > 0

    def __repr__(self) -> str: return f"""
surface: {self.surface.__repr__()} | base:{self.base.__repr__()},
hvc:{self.has_valid_candidates()},  
iw:{self.is_word} 
icc:{self.is_custom_compound})""".replace(newline, "")
