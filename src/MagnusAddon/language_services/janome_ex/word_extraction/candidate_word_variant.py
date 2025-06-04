from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.analysis_constants import noise_characters, non_word_characters
from language_services.janome_ex.word_extraction.dictionary_match import DictionaryMatch
from language_services.janome_ex.word_extraction.missing_match import MissingMatch
from language_services.janome_ex.word_extraction.vocab_match import VocabMatch
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.match import Match
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote

class CandidateWordVariant(Slots):
    __slots__ = ["__weakref__"]

    def __init__(self, candidate_word: WeakRef[CandidateWord], form: str, is_base: bool) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)

        self.is_base = is_base
        self.is_surface = not is_base
        self.weak_ref = WeakRef(self)
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index: int = candidate_word().start_location().character_start_index
        self.configuration: SentenceConfiguration = candidate_word().analysis().configuration
        self.candidate_word: WeakRef[CandidateWord] = candidate_word
        self.form: str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word(form)
        self.all_any_form_vocabs: list[VocabNote] = app.col().vocab.with_form(form)
        self.vocab_matches: list[VocabMatch] = [VocabMatch(self.weak_ref, vocab) for vocab in self.all_any_form_vocabs]

        def is_marked_incorrect_form(form_: str) -> bool:
            return self.configuration.incorrect_matches.excludes_at_index(form_, self.start_index)

        def is_marked_hidden_form(form_: str) -> bool:
            return self.configuration.hidden_matches.excludes_at_index(form_, self.start_index)

        self.unexcluded_any_form_vocabs: list[VocabNote] = [v for v in self.all_any_form_vocabs if not is_marked_incorrect_form(v.get_question())]
        self.unexcluded_form_owning_vocab: list[VocabNote] = [voc for voc in self.unexcluded_any_form_vocabs if voc.forms.is_owned_form(form)]
        self.excluded_vocabs: list[VocabNote] = [v for v in self.all_any_form_vocabs if is_marked_incorrect_form(v.get_question())]

        self.is_word: bool = self.dict_lookup.found_words() or len(self.all_any_form_vocabs) > 0
        self.is_marked_incorrect_by_config: bool = is_marked_incorrect_form(form)
        self.is_marked_hidden_by_config: bool = is_marked_hidden_form(form)

        self.exact_match_required_by_primary_form_vocab_configuration: bool = any(v for v in self.unexcluded_form_owning_vocab if v.matching_rules.requires_exact_match.is_set())

        self.prefix_is_not: set[str] = set().union(*[v.matching_rules.rules.prefix_is_not.get() for v in self.unexcluded_form_owning_vocab])
        self.is_excluded_by_prefix = any(excluded_prefix for excluded_prefix in self.prefix_is_not if self.preceding_surface.endswith(excluded_prefix))

        self.prefix_must_end_with: set[str] = set().union(*[v.matching_rules.rules.required_prefix.get() for v in self.unexcluded_form_owning_vocab])
        self.is_missing_required_prefix = self.prefix_must_end_with and not any(required for required in self.prefix_must_end_with if self.preceding_surface.endswith(required))

        self.is_strictly_suffix = any(voc for voc in self.unexcluded_form_owning_vocab if voc.matching_rules.is_strictly_suffix.is_set())
        self.requires_prefix = self.is_strictly_suffix or any(self.prefix_must_end_with)

        self.is_noise_character = self.form in noise_characters

        # will be completed in complete_analysis
        self.exact_match_required_by_counterpart_vocab_configuration: bool = False
        self.exact_match_required: bool = False
        self.is_exact_match_requirement_fulfilled: bool = False
        self.is_self_excluded = False
        self.completed_analysis = False
        self.is_valid_candidate: bool = False
        self.starts_with_non_word_token = self.candidate_word().start_location().token.is_non_word_character
        self.valid_vocab_matches: list[VocabMatch] = []
        self.form_owning_vocab_matches: list[VocabMatch] = []
        self.matches: list[Match] = []
        self.valid_matches: list[Match] = []

    @property
    def is_shadowed(self) -> bool:
        return (self.candidate_word().start_location().is_shadowed_by is not None
                or (self not in self.candidate_word().start_location().display_variants
                    and self.is_valid_candidate))

    def is_preliminarily_valid(self) -> bool:
        return (self.is_word and (not self.is_noise_character
                                  and not self.is_marked_incorrect_by_config
                                  and not self.is_self_excluded
                                  and not self.is_excluded_by_prefix
                                  and not self.is_missing_required_prefix
                                  and (not self.requires_prefix or self.has_prefix)
                                  and not self.starts_with_non_word_token
                                  ))

    def complete_analysis(self) -> None:
        if self.completed_analysis: return

        self.valid_vocab_matches = [vm for vm in self.vocab_matches if vm.is_valid]
        self.form_owning_vocab_matches = [vm for vm in self.vocab_matches if vm.vocab.forms.is_owned_form(self.form)]
        if any(self.valid_vocab_matches) or any(self.form_owning_vocab_matches):
            self.valid_matches = list(self.valid_vocab_matches)
            self.matches = list(self.vocab_matches)
            override_form = [df for df in self.valid_matches if df.parsed_form != self.form]
            if any(override_form):
                # todo: this is highly suspect, do we really want to just overwrite the parsed value? Should this logic not stay within the match?
                self.form = override_form[0].parsed_form
        else:
            dict_lookup = DictLookup.lookup_word(self.form)
            if dict_lookup.found_words():
                self.matches = [DictionaryMatch(self.weak_ref, dict_lookup.entries[0])]
                self.valid_matches = self.matches
            else:
                self.matches = [MissingMatch(self.weak_ref)]

        self.is_valid_candidate = (self.is_preliminarily_valid() and len(self.valid_matches) > 0)

        self.completed_analysis = True

    @property
    def has_prefix(self) -> bool:
        return self.preceding_surface != "" and self.preceding_surface[-1] not in non_word_characters

    @property
    def preceding_surface(self) -> str:
        previous = self.candidate_word().start_location().previous
        return previous().token.surface if previous else ""

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    def __repr__(self) -> str:
        return f"""{self.form}, is_valid_candidate:{self.is_valid_candidate}"""

class CandidateWordSurfaceVariant(CandidateWordVariant, Slots):
    def __init__(self, candidate_word: WeakRef[CandidateWord], form: str) -> None:
        super().__init__(candidate_word, form, is_base=False)

        if (not candidate_word().is_custom_compound
                and candidate_word().locations[-1]().token.do_not_match_surface_for_non_compound_vocab):
            self.is_self_excluded = True

class CandidateWordBaseVariant(CandidateWordVariant, Slots):
    def __init__(self, candidate_word: WeakRef[CandidateWord], form: str) -> None:
        super().__init__(candidate_word, form, is_base=True)

        self.surface_is_not: set[str] = set().union(*[v.matching_rules.rules.surface_is_not.get() for v in self.unexcluded_any_form_vocabs])
        self.surface_preferred_over_bases: set[str] = set()

    def complete_analysis(self) -> None:
        super().complete_analysis()

        if self.surface is not None:
            if self.surface.form in self.surface_is_not:
                self.is_self_excluded = True
                self.is_valid_candidate = False

            self.surface_preferred_over_bases = set().union(*[vocab.matching_rules.rules.prefer_over_base.get() for vocab in self.surface.unexcluded_any_form_vocabs])
            if self.form in self.surface_preferred_over_bases:
                self.is_valid_candidate = False

    @property
    def surface(self) -> CandidateWordVariant | None:
        return self.candidate_word().surface
