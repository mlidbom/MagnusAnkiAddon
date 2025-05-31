from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services import conjugator
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.analysis_constants import noise_characters, non_word_characters
from language_services.janome_ex.word_extraction.display_form import DisplayForm, MissingDisplayForm, VocabDisplayForm, DictionaryDisplayForm
from language_services.janome_ex.word_extraction.VocabCandidate import VocabCandidate
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils import kana_utils
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.location_range import LocationRange
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote

class CandidateWord(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, token_range: WeakRef[LocationRange], form: str, is_base: bool) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)

        self.is_base = is_base
        self.is_surface = not is_base
        self.weak_ref = WeakRef(self)
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index: int = token_range().start_location().character_start_index
        self.configuration: SentenceConfiguration = token_range().analysis().configuration
        self.token_range: WeakRef[LocationRange] = token_range
        self.form: str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word(form)
        self.all_any_form_vocabs: list[VocabNote] = app.col().vocab.with_form(form)

        self.vocab_candidates: list[VocabCandidate] = [VocabCandidate(self.weak_ref, voc) for voc in self.all_any_form_vocabs]

        def is_excluded_form(form_: str) -> bool:
            # todo: bug: With the current implementation this removes hidden matches from the parsed words. That is precisely what hidden matches should not do.
            return (self.configuration.incorrect_matches.excludes_at_index(form_, self.start_index)
                    or self.configuration.hidden_matches.excludes_at_index(form_, self.start_index))

        self.unexcluded_any_form_vocabs: list[VocabNote] = [v for v in self.all_any_form_vocabs if not is_excluded_form(v.get_question())]
        self.unexcluded_primary_form_vocabs: list[VocabNote] = [voc for voc in self.unexcluded_any_form_vocabs if voc.get_question() == form]
        self.excluded_vocabs: list[VocabNote] = [v for v in self.all_any_form_vocabs if is_excluded_form(v.get_question())]

        self.is_word: bool = self.dict_lookup.found_words() or len(self.all_any_form_vocabs) > 0
        self.is_excluded_by_config: bool = is_excluded_form(form)

        self.exact_match_required_by_primary_form_vocab_configuration: bool = any(v for v in self.unexcluded_primary_form_vocabs if v.matching_rules.requires_exact_match.is_set())

        self.prefix_is_not: set[str] = set().union(*[v.matching_rules.rules.prefix_is_not.get() for v in self.unexcluded_primary_form_vocabs])
        self.is_excluded_by_prefix = any(excluded_prefix for excluded_prefix in self.prefix_is_not if self.preceding_surface.endswith(excluded_prefix))

        self.prefix_must_end_with: set[str] = set().union(*[v.matching_rules.rules.required_prefix.get() for v in self.unexcluded_primary_form_vocabs])
        self.is_missing_required_prefix = self.prefix_must_end_with and not any(required for required in self.prefix_must_end_with if self.preceding_surface.endswith(required))

        self.is_strictly_suffix = any(voc for voc in self.unexcluded_primary_form_vocabs if voc.matching_rules.is_strictly_suffix.is_set())
        self.requires_prefix = self.is_strictly_suffix or any(self.prefix_must_end_with)

        self.is_noise_character = self.form in noise_characters

        # will be completed in complete_analysis
        self.exact_match_required_by_counterpart_vocab_configuration: bool = False
        self.exact_match_required: bool = False
        self.is_exact_match_requirement_fulfilled: bool = False
        self.is_self_excluded = False
        self.completed_analysis = False
        self.is_valid_candidate: bool = False
        self.is_shadowed: bool = False
        self.starts_with_non_word_token = self.token_range().start_location().token.is_non_word_character

        self.display_forms: list[DisplayForm] = []
        self.only_requires_being_a_word_to_be_a_valid_candidate = False

    @property
    def counterpart(self) -> CandidateWord: raise Exception("Not implemented")

    def complete_analysis(self) -> None:
        if self.completed_analysis: return

        self.is_shadowed = self.token_range().start_location().is_shadowed_by is not None

        self.exact_match_required_by_counterpart_vocab_configuration: bool = self.counterpart.exact_match_required_by_primary_form_vocab_configuration
        self.exact_match_required: bool = self.exact_match_required_by_primary_form_vocab_configuration or self.exact_match_required_by_counterpart_vocab_configuration
        self.is_exact_match_requirement_fulfilled: bool = self.form == self.counterpart.form or not self.exact_match_required

        if self.unexcluded_any_form_vocabs:
            self.display_forms = [VocabDisplayForm(self.weak_ref, voc) for voc in self.unexcluded_any_form_vocabs if self.vocab_fulfills_stem_requirements(voc)]
            override_form = [df for df in self.display_forms if df.parsed_form != self.form]
            if any(override_form):
                self.form = override_form[0].parsed_form
        else:
            dict_lookup = DictLookup.lookup_word(self.form)
            if dict_lookup.found_words():
                self.display_forms = [DictionaryDisplayForm(self.weak_ref, dict_lookup.entries[0])]
            else:
                self.display_forms = [MissingDisplayForm(self.weak_ref)]

        self.only_requires_being_a_word_to_be_a_valid_candidate = (not self.is_noise_character
                                                                   and not self.is_excluded_by_config
                                                                   and not self.is_self_excluded
                                                                   and not self.is_excluded_by_prefix
                                                                   and not self.is_missing_required_prefix
                                                                   and len(self.display_forms) > 0
                                                                   and (not self.requires_prefix or self.has_prefix)
                                                                   and not self.starts_with_non_word_token
                                                                   and self.is_exact_match_requirement_fulfilled)

        self.is_valid_candidate = self.only_requires_being_a_word_to_be_a_valid_candidate and self.is_word

        self.completed_analysis = True

    def vocab_fulfills_stem_requirements(self, vocab: VocabNote) -> bool:
        if vocab.matching_rules.requires_a_stem.is_set():
            return self.has_prefix and self.prefix[-1] in conjugator.a_stem_characters
        if vocab.matching_rules.requires_e_stem.is_set():
            return self.has_prefix and (self.prefix[-1] in conjugator.e_stem_characters or kana_utils.character_is_kanji(self.prefix[-1]))
        return True

    @property
    def has_prefix(self) -> bool: return self.preceding_surface != "" and self.preceding_surface[-1] not in non_word_characters

    @property
    def prefix(self) -> str: return self.preceding_surface[-1] if self.has_prefix else ""

    @property
    def preceding_surface(self) -> str:
        return self.token_range().start_location().previous().surface if self.token_range().start_location().previous else ""

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    def __repr__(self) -> str:
        return f"""CandidateWord:({self.form}, {self.is_valid_candidate})"""

class SurfaceCandidateWord(CandidateWord, Slots):
    def __init__(self, token_range: WeakRef[LocationRange]) -> None:
        super().__init__(token_range, "".join([t().surface for t in token_range().locations]) + "", is_base=False)

        if (not token_range().is_custom_compound
                and token_range().locations[-1]().token.do_not_match_surface_for_non_compound_vocab):
            self.is_self_excluded = True

    @property
    def counterpart(self) -> CandidateWord: return non_optional(self.token_range().base)

class BaseCandidateWord(CandidateWord, Slots):
    def __init__(self, token_range: WeakRef[LocationRange]) -> None:
        base_form = "".join([t().surface for t in token_range().locations[:-1]]) + token_range().locations[-1]().base
        if not token_range().is_custom_compound:
            base_form = token_range().locations[-1]().token.base_form_for_non_compound_vocab_matching

        super().__init__(token_range, base_form, is_base=True)

        self.surface_is_not: set[str] = set().union(*[v.matching_rules.rules.surface_is_not.get() for v in self.unexcluded_any_form_vocabs])
        self.surface_preferred_over_bases: set[str] = set()

    def complete_analysis(self) -> None:
        super().complete_analysis()

        if self.counterpart.form in self.surface_is_not:
            self.is_self_excluded = True
            self.is_valid_candidate = False

        self.surface_preferred_over_bases = set().union(*[vocab.matching_rules.rules.prefer_over_base.get() for vocab in self.counterpart.unexcluded_any_form_vocabs])
        if self.form in self.surface_preferred_over_bases:
            self.is_valid_candidate = False

    @property
    def counterpart(self) -> CandidateWord: return non_optional(self.token_range().surface)
