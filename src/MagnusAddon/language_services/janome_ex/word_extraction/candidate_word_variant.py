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
from sysutils.typed import non_optional
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

        self.start_index: int = word().start_location().character_start_index
        self.configuration: SentenceConfiguration = word().analysis().configuration
        self.word: WeakRef[CandidateWord] = word
        self.form: str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word(form)
        self.vocab_matches: list[VocabMatch] = [VocabMatch(self.weak_ref, vocab) for vocab in app.col().vocab.with_form(form)]
        self.form_owning_vocab_matches: list[VocabMatch] = [vm for vm in self.vocab_matches if vm.vocab.forms.is_owned_form(self.form)]

        self.is_known_word: bool = self.dict_lookup.found_words() or len(self.vocab_matches) > 0
        self.is_noise_character = self.form in noise_characters

        # will be completed in complete_analysis
        self.completed_analysis = False
        self.is_valid_candidate: bool = False
        self.valid_vocab_matches: list[VocabMatch] = []
        self.matches: list[Match] = []
        self.valid_matches: list[Match] = []

    @property
    def is_base(self) -> bool: return self.form == self.word().base_form
    @property
    def is_surface(self) -> bool: return self.form == self.word().surface_form
    @property
    def is_shadowed(self) -> bool: return self.is_shadowed_by is not None
    @property
    def shadowed_by_text(self) -> str: return non_optional(self.is_shadowed_by).form if self.is_shadowed else ""
    @property
    def is_shadowed_by(self) -> CandidateWordVariant | None:
        if any(self.word().start_location().is_shadowed_by):
            return self.word().start_location().is_shadowed_by[0]().display_variants[0]
        if (any(self.word().start_location().display_variants)
                and self.word().start_location().display_variants[0].word().location_count > self.word().location_count):
            return self.word().start_location().display_variants[0]
        return None
    @property
    def is_preliminarily_valid(self) -> bool: return self.is_known_word and not self.word().starts_with_non_word_character

    @property
    def vocabs_control_match_status(self) -> bool:
        return (any(self.valid_vocab_matches)
                or any(self.form_owning_vocab_matches)
                or (any(self.vocab_matches) and not self.dict_lookup.found_words() and self.word().is_custom_compound))

    def complete_analysis(self) -> None:
        if self.completed_analysis: return

        self.valid_vocab_matches = [vm for vm in self.vocab_matches if vm.is_valid]
        if self.vocabs_control_match_status:
            self.valid_matches = list(self.valid_vocab_matches)
            self.matches = list(self.vocab_matches)
        else:
            if self.dict_lookup.found_words():
                self.matches = [DictionaryMatch(self.weak_ref, self.dict_lookup.entries[0])]
                self.valid_matches = self.matches
            else:
                self.matches = [MissingMatch(self.weak_ref)]

        self.is_valid_candidate = self.is_preliminarily_valid and any(self.valid_matches)

        self.completed_analysis = True

    @property
    def display_matches(self) -> list[Match]:
        ex_assert.that(self.completed_analysis)
        return [match for match in self.matches if match.is_displayed]

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    def __repr__(self) -> str:
        return f"""{self.form}, is_valid_candidate:{self.is_valid_candidate}"""
