from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabnote import VocabNote

class CandidateForm:
    def __init__(self, candidate: CandidateWord, is_surface: bool, form:str):
        from ankiutils import app
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.exclusions = candidate.analysis.exclusions
        self.candidate = candidate
        self.is_surface = is_surface
        self.form = form

        self.dict_lookup:DictLookup = DictLookup.lookup_word_shallow(form)
        self.vocabs:list[VocabNote] = app.col().vocab.with_form(form)

        self.is_word:bool = self.dict_lookup.found_words() or len(self.vocabs) > 0
        self.is_excluded_by_config:bool = form in self.exclusions

    def is_valid_candidate(self) -> bool: return self.is_word and not self.is_excluded_by_config
    def has_vocabs(self) -> bool: return len(self.vocabs) > 0

    def __repr__(self) -> str:
        return f"""{self.form}"""


class SurfaceCandidateForm(CandidateForm):
    def __init__(self, candidate: CandidateWord):
        super().__init__(candidate, True, "".join([t.surface for t in candidate.locations]) + "")

class BaseCandidateForm(CandidateForm):
    def __init__(self, candidate: CandidateWord):
        super().__init__(candidate, False, "".join([t.surface for t in candidate.locations[:-1]]) + candidate.locations[-1].base)