from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from sysutils import kana_utils

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_entry import DictEntry
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class WordMatch(Slots):
    def __init__(self, candidate: WeakRef[CandidateWord]) -> None:
        self.candidate: WeakRef[CandidateWord] = candidate
        self.parsed_form: str = candidate().form
        self.vocab_form: str = ""
        self.answer: str = ""
        self.readings: list[str] = []

class VocabWordMatch(WordMatch):
    def __init__(self, candidate: WeakRef[CandidateWord], vocab: VocabNote) -> None:
        super().__init__(candidate)
        self.vocab: VocabNote = vocab
        self.vocab_form = vocab.get_question()
        self.answer = vocab.get_answer()
        self.readings = vocab.readings.get()

        if vocab.matching_rules.question_overrides_form.is_set():
            self.parsed_form = self.vocab.get_question()

        self.is_valid = self.vocab_fulfills_stem_requirements(vocab)

    @property
    def has_prefix(self) -> bool:
        return self.candidate().has_prefix

    @property
    def prefix(self) -> str:
        return self.candidate().prefix

    def vocab_fulfills_stem_requirements(self, vocab: VocabNote) -> bool:
        fulfills_requirements = True
        if vocab.matching_rules.forbids_a_stem.is_set():
            fulfills_requirements = fulfills_requirements and (not self.has_prefix or self.prefix[-1] not in conjugator.a_stem_characters)
        if vocab.matching_rules.requires_a_stem.is_set():
            fulfills_requirements = fulfills_requirements and (self.has_prefix and self.prefix[-1] in conjugator.a_stem_characters)
        if vocab.matching_rules.requires_e_stem.is_set():
            fulfills_requirements = fulfills_requirements and (self.has_prefix and (self.prefix[-1] in conjugator.e_stem_characters or kana_utils.character_is_kanji(self.prefix[-1])))
        return fulfills_requirements

class DictionaryWordMatch(WordMatch, Slots):
    def __init__(self, candidate: WeakRef[CandidateWord], dictionary_entry: DictEntry) -> None:
        super().__init__(candidate)
        self.dictionary_entry: DictEntry = dictionary_entry
        self.answer: str = dictionary_entry.generate_answer()
        self.readings: list[str] = [f.text for f in dictionary_entry.entry.kana_forms]

class MissingWordMatch(WordMatch):
    def __init__(self, candidate: WeakRef[CandidateWord]) -> None:
        super().__init__(candidate)
        self.answer = "---"
