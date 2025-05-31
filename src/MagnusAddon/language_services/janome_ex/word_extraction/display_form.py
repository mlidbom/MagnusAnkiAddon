from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_entry import DictEntry
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class DisplayForm(Slots):
    def __init__(self, candidate: WeakRef[CandidateWord]) -> None:
        self.candidate: WeakRef[CandidateWord] = candidate
        self.parsed_form: str = candidate().form
        self.vocab_form: str = ""
        self.answer: str = ""
        self.readings: list[str] = []

class VocabDisplayForm(DisplayForm):
    def __init__(self, candidate: WeakRef[CandidateWord], vocab: VocabNote) -> None:
        super().__init__(candidate)
        self.vocab: VocabNote = vocab
        self.vocab_form = vocab.get_question()
        self.answer = vocab.get_answer()
        self.readings = vocab.readings.get()

        if vocab.matching_rules.question_overrides_form.is_set():
            self.parsed_form = self.vocab.get_question()

class DictionaryDisplayForm(DisplayForm, Slots):
    def __init__(self, candidate: WeakRef[CandidateWord], dictionary_entry: DictEntry) -> None:
        super().__init__(candidate)
        self.dictionary_entry: DictEntry = dictionary_entry
        self.answer: str = dictionary_entry.generate_answer()
        self.readings: list[str] = [f.text for f in dictionary_entry.entry.kana_forms]

class MissingDisplayForm(DisplayForm):
    def __init__(self, candidate: WeakRef[CandidateWord]) -> None:
        super().__init__(candidate)
        self.answer = "---"
