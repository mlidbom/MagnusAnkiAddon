from __future__ import annotations
from typing import TYPE_CHECKING

from language_services.jamdict_ex.dict_entry import DictEntry

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_form import CandidateForm
    from note.vocabnote import VocabNote

class DisplayForm:
    def __init__(self, candidate: CandidateForm):
        self.candidate:CandidateForm = candidate
        self.parsed_form:str = candidate.form
        self.vocab_form:str = ""
        self.answer: str = ""


class VocabDisplayForm(DisplayForm):
    def __init__(self, candidate: CandidateForm, vocab: VocabNote):
        super().__init__(candidate)
        self.vocab:VocabNote = vocab
        self.vocab_form = vocab.get_question()
        self.answer = vocab.get_answer()

        if vocab.is_question_overrides_form():
            self.parsed_form = self.vocab.get_question()


class DictionaryDisplayForm(DisplayForm):
    def __init__(self, candidate: CandidateForm, dictionary_entry: DictEntry):
        super().__init__(candidate)
        self.dictionary_entry = dictionary_entry

class MissingDisplayForm(DisplayForm):
    def __init__(self, candidate: CandidateForm):
        super().__init__(candidate)
        self.answer = "---"
