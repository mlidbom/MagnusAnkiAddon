from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextLocation

class CandidateWord:
    def __init__(self, locations: list[TextLocation]):
        from ankiutils import app
        from language_services.jamdict_ex.dict_lookup import DictLookup
        self.analysis = locations[0].analysis
        self.location = locations
        self.surface = "".join([t.surface for t in locations]) + ""
        self.base = "".join([t.surface for t in locations[:-1]]) + locations[-1].base

        self.surface_dict_lookup = DictLookup.lookup_word_shallow(self.surface)
        self.base_dict_lookup = DictLookup.lookup_word_shallow(self.base)
        self.surface_vocabs = app.col().vocab.with_form(self.surface)
        self.base_vocabs = app.col().vocab.with_form(self.base)

    def surface_is_word(self) -> bool: return self.surface_dict_lookup.found_words() or len(self.surface_vocabs) > 0
    def base_is_word(self) -> bool: return self.base_dict_lookup.found_words() or len(self.base_vocabs) > 0
    def is_word(self) -> bool: return self.surface_is_word() or self.base_is_word()
    def surface_is_excluded(self) -> bool: return self.surface in self.analysis.exclusions
    def base_is_excluded(self) -> bool: return self.base in self.analysis.exclusions

    def base_is_valid_candidate(self) -> bool: return self.base_is_word() and not self.base_is_excluded()
    def surface_is_valid_candidate(self) -> bool: return self.surface_is_word() and not self.surface_is_excluded()
    def has_valid_candidates(self) -> bool: return self.base_is_valid_candidate() or self.surface_is_valid_candidate()

    def __repr__(self) -> str: return f"""CandidateWord('{self.surface}, {self.base}')"""
