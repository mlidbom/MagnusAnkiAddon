from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services.janome_ex.word_extraction.analysis_constants import noise_characters
from language_services.janome_ex.word_extraction.dictionary_match import DictionaryMatch
from language_services.janome_ex.word_extraction.missing_match import MissingMatch
from language_services.janome_ex.word_extraction.vocab_match import VocabMatch
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_lookup import DictLookup
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote

class CandidateWordVariant(WeakRefable, Slots):
    def __init__(self, word: WeakRef[CandidateWord], form: str, is_base: bool) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)

        self.is_base = is_base
        self.is_surface = not is_base
        self.weak_ref = WeakRef(self)
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index: int = word().start_location().character_start_index
        self.configuration: SentenceConfiguration = word().analysis().configuration
        self.word: WeakRef[CandidateWord] = word
        self.form: str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word(form)
        self.all_any_form_vocabs: list[VocabNote] = app.col().vocab.with_form(form)
        self.vocab_matches: list[VocabMatch] = [VocabMatch(self.weak_ref, vocab) for vocab in self.all_any_form_vocabs]
        self.form_owning_vocab_matches: list[VocabMatch] = [vm for vm in self.vocab_matches if vm.vocab.forms.is_owned_form(self.form)]

        def is_marked_incorrect_form(form_: str) -> bool:
            return self.configuration.incorrect_matches.excludes_at_index(form_, self.start_index)

        self.unexcluded_any_form_vocabs: list[VocabNote] = [v for v in self.all_any_form_vocabs if not is_marked_incorrect_form(v.get_question())]
        self.unexcluded_form_owning_vocab: list[VocabNote] = [voc for voc in self.unexcluded_any_form_vocabs if voc.forms.is_owned_form(form)]

        self.is_word: bool = self.dict_lookup.found_words() or len(self.all_any_form_vocabs) > 0


        #todo: move into match requirements
        self.prefix_is_not: set[str] = set().union(*[v.matching_rules.rules.prefix_is_not.get() for v in self.unexcluded_form_owning_vocab])
        self.is_excluded_by_prefix = any(excluded_prefix for excluded_prefix in self.prefix_is_not if self.preceding_surface.endswith(excluded_prefix))

        self.is_noise_character = self.form in noise_characters

        # will be completed in complete_analysis
        self.exact_match_required_by_counterpart_vocab_configuration: bool = False
        self.exact_match_required: bool = False
        self.is_exact_match_requirement_fulfilled: bool = False
        self.completed_analysis = False
        self.is_valid_candidate: bool = False
        self.starts_with_non_word_token = self.word().start_location().token.is_non_word_character
        self.valid_vocab_matches: list[VocabMatch] = []
        self.matches: list[Match] = []
        self.valid_matches: list[Match] = []

    @property
    def is_shadowed(self) -> bool:
        return (self.word().start_location().is_shadowed_by is not None
                or (self not in self.word().start_location().display_variants
                    and self.is_valid_candidate))

    def is_preliminarily_valid(self) -> bool:
        return (self.is_word and not (self.is_noise_character
                                      or self.is_excluded_by_prefix
                                      or self.starts_with_non_word_token))

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

        self.is_valid_candidate = self.is_preliminarily_valid() and any(self.valid_matches)

        self.completed_analysis = True

    @property
    def display_matches(self) -> list[Match]:
        return [match for match in self.matches if match.is_displayed]

    @property
    def preceding_surface(self) -> str:
        previous = self.word().start_location().previous
        return previous().token.surface if previous else ""

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    def __repr__(self) -> str:
        return f"""{self.form}, is_valid_candidate:{self.is_valid_candidate}"""

class CandidateWordSurfaceVariant(CandidateWordVariant, Slots):
    def __init__(self, word: WeakRef[CandidateWord], form: str) -> None:
        super().__init__(word, form, is_base=False)

class CandidateWordBaseVariant(CandidateWordVariant, Slots):
    def __init__(self, word: WeakRef[CandidateWord], form: str) -> None:
        super().__init__(word, form, is_base=True)
