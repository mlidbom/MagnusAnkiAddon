from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services.janome_ex.word_extraction.analysis_constants import noise_characters
from language_services.janome_ex.word_extraction.matches.dictionary_match import DictionaryMatch
from language_services.janome_ex.word_extraction.matches.missing_match import MissingMatch
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils import ex_assert
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_lookup import DictLookup
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.matches.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration

class CandidateWordVariant(WeakRefable, Slots):
    def __init__(self, word: WeakRef[CandidateWord], form: str) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)

        self.weak_ref = WeakRef(self)
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index: int = word().start_location.character_start_index
        self.configuration: SentenceConfiguration = word().analysis.configuration
        self.word: WeakRef[CandidateWord] = word
        self.form: str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word(form)
        self.vocab_matches: list[VocabMatch] = [VocabMatch(self.weak_ref, vocab) for vocab in app.col().vocab.with_form(form)]
        self.form_owning_vocab_matches: list[VocabMatch] = [vm for vm in self.vocab_matches if vm.vocab.forms.is_owned_form(self.form)]

        self.is_known_word: bool = self.dict_lookup.found_words() or len(self.vocab_matches) > 0
        self.is_noise_character = self.form in noise_characters

        # will be completed in complete_analysis
        self.completed_analysis = False
        self.matches: list[Match] = []
        self.valid_matches: list[Match] = []

    @property
    def is_surface(self) -> bool: return self.form == self.word().surface_form
    @property
    def vocabs_control_match_status(self) -> bool:
        return (any(self.valid_vocab_matches)
                or any(self.form_owning_vocab_matches)
                or (any(self.vocab_matches) and not self.dict_lookup.found_words() and self.word().is_custom_compound))

    def run_validity_analysis(self) -> None:
        if self.completed_analysis: return

        if self.vocabs_control_match_status:
            self.valid_matches = list(self.valid_vocab_matches)
            self.matches = list(self.vocab_matches)
        else:
            if self.dict_lookup.found_words():
                self.matches = [DictionaryMatch(self.weak_ref, self.dict_lookup.entries[0])]
                self.valid_matches = self.matches
            else:
                self.matches = [MissingMatch(self.weak_ref)]

        self.completed_analysis = True

    @property
    def valid_vocab_matches(self) -> list[VocabMatch]: return [vm for vm in self.vocab_matches if vm.is_valid]
    @property
    def is_valid(self) -> bool: return any(self.valid_matches)

    @property
    def _once_analyzed(self) -> CandidateWordVariant:
        ex_assert.that(self.completed_analysis)
        return self

    @property
    def display_matches(self) -> list[Match]: return [match for match in self._once_analyzed.matches if match.is_displayed]

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    def __repr__(self) -> str:
        return f"""{self.form}, is_valid_candidate:{self.is_valid}"""
