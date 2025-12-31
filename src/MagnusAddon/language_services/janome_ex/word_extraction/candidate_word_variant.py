from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.dictionary_match import DictionaryMatch
from language_services.janome_ex.word_extraction.matches.missing_match import MissingMatch
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils import ex_assert
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_lookup_result import DictLookupResult
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.matches.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration

@final
class CandidateWordVariant(WeakRefable, Slots):
    def __init__(self, word: WeakRef[CandidateWord], form: str) -> None:
        self.weak_ref = WeakRef(self)
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self._word: WeakRef[CandidateWord] = word
        self.form: str = form

        self._dict_lookup: Lazy[DictLookupResult] = Lazy(lambda: DictLookup.lookup_word(form))
        self.vocab_matches: QList[VocabMatch] = QList(VocabMatch(self.weak_ref, vocab) for vocab in app.col().vocab.with_form(form))

        # will be completed in complete_analysis
        self.completed_validity_analysis = False
        self.completed_visibility_analysis = False
        self.matches: QList[Match] = QList()
        self._is_valid: bool = False
        self._valid_matches: QList[Match] = QList()
        self._display_matches: QList[Match] = QList()

    @property
    def is_surface(self) -> bool: return self.form == self.word.surface_form
    @property
    def vocabs_control_match_status(self) -> bool:
        return (any(self._valid_vocab_matches)
                or any(self._form_owning_vocab_matches)
                or (any(self.vocab_matches) and not self._dict_lookup().found_words() and self.word.is_custom_compound))

    def run_validity_analysis(self) -> None:
        ex_assert.that(not self.completed_validity_analysis)

        if self.vocabs_control_match_status:
            self.matches = QList(self.vocab_matches)
        else:
            if self._dict_lookup().found_words():
                self.matches = QList([DictionaryMatch(self.weak_ref, self._dict_lookup().entries[0])])
            else:
                self.matches = QList([MissingMatch(self.weak_ref)])

        self.completed_validity_analysis = True
        self._is_valid = any(match for match in self._once_validity_analyzed.matches if match.is_valid)
        self._valid_matches = self.matches.where(lambda match: match.is_valid).to_list()

    def run_visibility_analysis(self) -> None:
        self._display_matches = self._once_validity_analyzed.matches.where(lambda it: it.is_displayed).to_list()
        self.completed_visibility_analysis = True

    @property
    def start_index(self) -> int: return self.word.start_location.character_start_index
    @property
    def configuration(self) -> SentenceConfiguration: return self.word.analysis.configuration
    @property
    def word(self) -> CandidateWord: return self._word()
    @property
    def is_known_word(self) -> bool: return len(self.vocab_matches) > 0 or self._dict_lookup().found_words()
    @property
    def _form_owning_vocab_matches(self) -> list[VocabMatch]: return [vm for vm in self.vocab_matches if vm.vocab.forms.is_owned_form(self.form)]
    @property
    def _valid_vocab_matches(self) -> list[VocabMatch]: return [vm for vm in self.vocab_matches if vm.is_valid]
    @property
    def has_valid_match(self) -> bool: return self._once_validity_analyzed._is_valid
    @property
    def valid_matches(self) -> QList[Match]: return self._once_validity_analyzed._valid_matches
    @property
    def display_matches(self) -> QList[Match]: return self._once_visibility_analyzed._display_matches

    @property
    def _once_validity_analyzed(self) -> CandidateWordVariant:
        if not self.completed_validity_analysis: raise Exception("Analysis not completed yet")
        return self

    @property
    def _once_visibility_analyzed(self) -> CandidateWordVariant:
        if not self.completed_validity_analysis: raise Exception("Analysis not completed yet")
        return self

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    @override
    def __repr__(self) -> str:
        return f"""{self.form}, is_valid_candidate:{self.has_valid_match}"""
