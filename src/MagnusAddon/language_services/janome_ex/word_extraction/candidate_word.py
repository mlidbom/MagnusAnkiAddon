from __future__ import annotations
from typing import TYPE_CHECKING
from language_services.janome_ex.word_extraction.display_word import BaseCandidateForm, CandidateForm, SurfaceCandidateForm

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.text_location import TextLocation

from sysutils.ex_str import newline

class CandidateWord:
    def __init__(self, locations: list[TextLocation]):
        self.analysis: TextAnalysis = locations[0].analysis
        self.locations: list[TextLocation] = locations
        self.is_custom_compound: bool = len(locations) > 1

        self.surface: SurfaceCandidateForm = SurfaceCandidateForm(self)
        self.base: BaseCandidateForm = BaseCandidateForm(self)

        self.is_word: bool = self.surface.is_word or self.base.is_word

        self.display_words: list[CandidateForm] = []
        if self.base.is_valid_candidate():
            self.display_words.append(self.base)
        if self.surface.is_valid_candidate():
            self.display_words.append(self.surface)

    def has_valid_candidates(self) -> bool: return self.base.is_valid_candidate() or self.surface.is_valid_candidate()

    def __repr__(self) -> str: return f"""
surface: {self.surface.__repr__()} | base:{self.base.__repr__()},
hvc:{self.has_valid_candidates()},  
iw:{self.is_word} 
icc:{self.is_custom_compound})""".replace(newline, "")
