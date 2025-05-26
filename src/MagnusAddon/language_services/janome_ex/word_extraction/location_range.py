from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.candidate_word import BaseCandidateWord, CandidateWord, SurfaceCandidateWord
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from language_services.janome_ex.word_extraction.text_location import TokenTextLocation

from sysutils.ex_str import newline


class LocationRange(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, locations: list[WeakRef[TokenTextLocation]]) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.analysis: WeakRef[TextAnalysis] = locations[0]().analysis
        self.locations: list[WeakRef[TokenTextLocation]] = locations
        self.is_custom_compound: bool = len(locations) > 1
        self.start_location: WeakRef[TokenTextLocation] = self.locations[0]
        self.end_location: WeakRef[TokenTextLocation] = self.locations[-1]
        self.length = len(self.locations)

        self.base: CandidateWord = BaseCandidateWord(WeakRef(self))
        self.surface: CandidateWord = SurfaceCandidateWord(WeakRef(self)) if self.end_location().surface != self.end_location().base else self.base

        self.is_word: bool = self.surface.is_word or self.base.is_word

        self.is_inflectable_word: bool = self.end_location().token.is_inflectable_word
        self.next_token_is_inflecting_word: bool = self.end_location().is_next_location_inflecting_word()
        self.is_inflected_word: bool = self.is_inflectable_word and self.next_token_is_inflecting_word

        self.should_include_surface_in_all_words: bool = False
        self.should_include_base_in_all_words: bool = False
        self.all_words: list[CandidateWord] = []
        self.display_words: list[CandidateWord] = []

    def complete_analysis(self) -> None:
        self.base.complete_analysis()
        self.surface.complete_analysis()

        #todo: bug: if the surface is not a valid candidate, the word is inflected, and the base is not a valid candidate, no words are included
        self.should_include_surface_in_all_words = (self.surface.is_valid_candidate
                                                    and not self.is_inflected_word
                                                    and self.surface.form != self.base.form)
        self.should_include_base_in_all_words = self.base.is_valid_candidate

        self.all_words = []
        if self.should_include_base_in_all_words:
            self.all_words.append(self.base)
        if self.should_include_surface_in_all_words:
            self.all_words.append(self.surface)

        #todo: may result in no matches, and I'm not sure we should say that only one is ever allowed to be included
        if self.should_include_surface_in_all_words:
            self.display_words.append(self.surface)
        elif self.should_include_base_in_all_words:
            self.display_words.append(self.base)

    def has_valid_words(self) -> bool: return len(self.all_words) > 0

    def __repr__(self) -> str: return f"""
surface: {self.surface.__repr__()} | base:{self.base.__repr__()},
hvc:{self.has_valid_words()},
iw:{self.is_word}
icc:{self.is_custom_compound})""".replace(newline, "")
