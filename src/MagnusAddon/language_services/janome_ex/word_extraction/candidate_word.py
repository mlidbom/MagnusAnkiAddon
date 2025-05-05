from __future__ import annotations
from typing import TYPE_CHECKING
from language_services.janome_ex.word_extraction.display_word import BaseCandidateForm, CandidateForm, SurfaceCandidateForm

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextLocation
    from note.vocabnote import VocabNote

from sysutils.ex_str import newline

class CandidateWord:
    def __init__(self, locations: list[TextLocation]):
        from ankiutils import app
        from language_services.jamdict_ex.dict_lookup import DictLookup
        self.analysis = locations[0].analysis
        self.locations = locations
        self.is_custom_compound = len(locations) > 1

        self.surface_str:str = "".join([t.surface for t in locations]) + ""
        self.base_str:str = "".join([t.surface for t in locations[:-1]]) + locations[-1].base

        self.surface_dict_lookup:DictLookup = DictLookup.lookup_word_shallow(self.surface_str)
        self.base_dict_lookup:DictLookup = DictLookup.lookup_word_shallow(self.base_str)
        self.surface_vocabs:list[VocabNote] = app.col().vocab.with_form(self.surface_str)
        self.base_vocabs:list[VocabNote] = app.col().vocab.with_form(self.base_str)

        self.surface_is_word = self.surface_dict_lookup.found_words() or len(self.surface_vocabs) > 0
        self.base_is_word = self.base_dict_lookup.found_words() or len(self.base_vocabs) > 0
        self.is_word = self.surface_is_word or self.base_is_word
        self.surface_is_excluded_by_config = self.surface_str in self.analysis.exclusions
        self.base_is_excluded_by_config = self.base_str in self.analysis.exclusions

        self.surface = SurfaceCandidateForm(self)
        self.base = BaseCandidateForm(self)

        self.display_words:list[CandidateForm] = []
        if self.base_is_valid_candidate():
            self.display_words.append(CandidateForm(self, False))
        if self.surface_is_valid_candidate():
            self.display_words.append(CandidateForm(self, True))

    def surface_has_vocab(self) -> bool: return len(self.surface_vocabs) > 0
    def base_has_vocab(self) -> bool: return len(self.base_vocabs) > 0

    def base_is_valid_candidate(self) -> bool: return self.base_is_word and not self.base_is_excluded_by_config
    def surface_is_valid_candidate(self) -> bool: return self.surface_is_word and not self.surface_is_excluded_by_config
    def has_valid_candidates(self) -> bool: return self.base_is_valid_candidate() or self.surface_is_valid_candidate()

    def __repr__(self) -> str: return f"""
CandidateWord({self.surface_str} | {self.base_str},
hvc:{self.has_valid_candidates()},  
bivc:{self.base_is_valid_candidate()}, 
sivc:{self.surface_is_valid_candidate()}, 
iw:{self.is_word} 
siw:{self.surface_is_word}, 
biw:{self.base_is_word} 
sie:{self.surface_is_excluded_by_config}, 
bie:{self.base_is_excluded_by_config} 
icc:{self.is_custom_compound})""".replace(newline, "")
