from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabnote import VocabNote

from sysutils.ex_str import newline

class CandidateForm:
    def __init__(self, candidate: CandidateWord, is_surface: bool, form: str):
        from ankiutils import app
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index = candidate.locations[0].start_index
        self.configuration_exclusions = candidate.analysis.exclusions
        self.candidate = candidate
        self.is_surface = is_surface
        self.form = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word_shallow(form)
        self.all_vocabs: list[VocabNote] = app.col().vocab.with_form(form)

        def is_excluded_form(form_: str) -> bool:
            return any(exclusion for exclusion in self.configuration_exclusions if exclusion.excludes_form_at_index(form_, self.start_index))

        self.unexcluded_vocabs:list[VocabNote] = [v for v in self.all_vocabs if not is_excluded_form(v.get_question())]

        self.forms_excluded_by_vocab_configuration:set[str] = set().union(*[v.get_excluded_forms() for v in self.unexcluded_vocabs])

        self.is_word: bool = self.dict_lookup.found_words() or len(self.all_vocabs) > 0
        self.is_excluded_by_config: bool = is_excluded_form(form)
        self.is_self_excluded: bool = form in self.forms_excluded_by_vocab_configuration

    def is_valid_candidate(self) -> bool: return (self.is_word
                                                  and not self.is_excluded_by_config
                                                  and not self.is_self_excluded)

    def __repr__(self) -> str:
        return f"""CandidateForm: {self.form}, ivc:{self.is_valid_candidate()}, iw:{self.is_word} ie:{self.is_excluded_by_config}""".replace(newline, "")

class SurfaceCandidateForm(CandidateForm):
    def __init__(self, candidate: CandidateWord):
        super().__init__(candidate, True, "".join([t.surface for t in candidate.locations]) + "")

class BaseCandidateForm(CandidateForm):
    def __init__(self, candidate: CandidateWord):
        super().__init__(candidate, False, "".join([t.surface for t in candidate.locations[:-1]]) + candidate.locations[-1].base)
