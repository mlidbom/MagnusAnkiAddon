from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services import conjugator
from language_services.janome_ex.word_extraction.display_form import DisplayForm, MissingDisplayForm, VocabDisplayForm
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils import kana_utils
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.sentences.sentence_configuration import SentenceConfiguration
    from note.vocabulary.vocabnote import VocabNote

from sysutils.ex_str import newline

_noise_characters = {".", ",", ":", ";", "/", "|", "。", "、", "?", "!"}
_non_word_characters = _noise_characters | {" ", "\t"}
class CandidateForm(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, candidate: WeakRef[CandidateWord], is_surface: bool, form: str) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index: int = candidate().locations[0]().character_start_index
        self.configuration: SentenceConfiguration = candidate().analysis().configuration
        self.candidate: WeakRef[CandidateWord] = candidate
        self.is_surface: bool = is_surface
        self.form: str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word_shallow(form)
        self.all_vocabs: list[VocabNote] = app.col().vocab.with_form(form)

        def is_excluded_form(form_: str) -> bool:
            # todo: bug: With the current implementation this removes hidden matches from the parsed words. That is precisely what hidden matches should not do.
            return (self.configuration.incorrect_matches.excludes_at_index(form_, self.start_index)
                    or self.configuration.hidden_matches.excludes_at_index(form_, self.start_index))

        self.unexcluded_vocabs: list[VocabNote] = [v for v in self.all_vocabs if not is_excluded_form(v.get_question())]
        self.excluded_vocabs: list[VocabNote] = [v for v in self.all_vocabs if is_excluded_form(v.get_question())]

        self.is_word: bool = self.dict_lookup.found_words() or len(self.all_vocabs) > 0
        self.is_excluded_by_config: bool = is_excluded_form(form)

        self.forms_excluded_by_compound_root_vocab_configuration: set[str] = set()
        self.is_excluded_by_compound_root_vocab_configuration: bool = False
        self.exact_match_required_by_vocab_configuration: bool = any(v for v in self.unexcluded_vocabs if v.meta_data.flags.requires_exact_match())
        self.exact_match_required_by_counterpart_vocab_configuration: bool = False
        self.exact_match_required: bool = False
        self.is_exact_match_requirement_fulfilled: bool = False

        self.prefix_is_not: set[str] = set().union(*[v.matching_rules.rules.prefix_is_not.get() for v in self.unexcluded_vocabs])
        self.is_excluded_by_prefix = any(excluded_prefix for excluded_prefix in self.prefix_is_not if self.preceding_surface.endswith(excluded_prefix))

        self.required_prefix: set[str] = set().union(*[v.matching_rules.rules.required_prefix.get() for v in self.unexcluded_vocabs])
        self.is_missing_required_prefix = self.required_prefix and not any(required for required in self.required_prefix if self.preceding_surface.endswith(required))

        self.display_forms: list[DisplayForm] = []
        self.is_self_excluded = False
        self.completed_analysis = False

    def counterpart(self) -> CandidateForm: raise Exception("Not implemented")

    def complete_analysis(self) -> None:
        if self.completed_analysis: return
        self.is_excluded_by_compound_root_vocab_configuration: bool = self.form in self.forms_excluded_by_compound_root_vocab_configuration
        self.exact_match_required_by_counterpart_vocab_configuration: bool = self.counterpart().exact_match_required_by_vocab_configuration
        self.exact_match_required: bool = self.exact_match_required_by_vocab_configuration or self.exact_match_required_by_counterpart_vocab_configuration
        self.is_exact_match_requirement_fulfilled: bool = self.form == self.counterpart().form or not self.exact_match_required

        if self.unexcluded_vocabs:
            self.display_forms = [VocabDisplayForm(WeakRef(self), voc) for voc in self.unexcluded_vocabs if self.vocab_fulfills_stem_requirements(voc)]
            override_form = [df for df in self.display_forms if df.parsed_form != self.form]
            if any(override_form):
                self.form = override_form[0].parsed_form
        else:
            self.display_forms = [MissingDisplayForm(WeakRef(self))]

        self.completed_analysis = True

    def vocab_fulfills_stem_requirements(self, vocab: VocabNote) -> bool:
        if vocab.matching_rules.requires_a_stem.is_set:
            return self.has_prefix and self.prefix[-1] in conjugator.a_stem_characters
        if vocab.matching_rules.requires_e_stem.is_set:
            return self.has_prefix and self.prefix[-1] in conjugator.e_stem_characters or kana_utils.character_is_kanji(self.prefix[-1])
        return True

    @property
    def has_prefix(self) -> bool: return self.preceding_surface != "" and self.preceding_surface[-1] not in _non_word_characters

    @property
    def prefix(self) -> str: return self.preceding_surface[-1] if self.has_prefix else ""

    def is_valid_candidate(self) -> bool:
        return ((self.is_word or not self.candidate().is_custom_compound)
                and self.form not in _noise_characters
                and not self.is_excluded_by_config
                and not self.is_self_excluded
                and not self.is_excluded_by_prefix
                and not self.is_missing_required_prefix
                and not self.is_excluded_by_compound_root_vocab_configuration
                and self.is_exact_match_requirement_fulfilled)

    @property
    def preceding_surface(self) -> str:
        return self.candidate().start_location().previous().surface if self.candidate().start_location().previous else ""

    def to_exclusion(self) -> WordExclusion:
        return WordExclusion.at_index(self.form, self.start_index)

    def __repr__(self) -> str:
        return f"""CandidateForm: {self.form}, ivc:{self.is_valid_candidate()}, iw:{self.is_word} ie:{self.is_excluded_by_config}""".replace(newline, "")

class SurfaceCandidateForm(CandidateForm, Slots):
    def __init__(self, candidate: WeakRef[CandidateWord]) -> None:
        super().__init__(candidate, True, "".join([t().surface for t in candidate().locations]) + "")

        if (not candidate().is_custom_compound
                and candidate().locations[-1]().token.do_not_match_surface_for_non_compound_vocab):
            self.is_self_excluded = True

    def counterpart(self) -> CandidateForm: return non_optional(self.candidate().base)

class BaseCandidateForm(CandidateForm, Slots):
    def __init__(self, candidate: WeakRef[CandidateWord]) -> None:
        base_form = "".join([t().surface for t in candidate().locations[:-1]]) + candidate().locations[-1]().base
        if not candidate().is_custom_compound:
            base_form = candidate().locations[-1]().token.base_form_for_non_compound_vocab_matching

        super().__init__(candidate, False, base_form)

        self.surface_is_not: set[str] = set().union(*[v.matching_rules.rules.surface_is_not.get() for v in self.unexcluded_vocabs])
        self.surface_preferred_over_bases: set[str] = set()

    def complete_analysis(self) -> None:
        super().complete_analysis()

        if self.counterpart().form in self.surface_is_not:
            self.is_self_excluded = True

        self.surface_preferred_over_bases = set().union(*[vocab.matching_rules.rules.prefer_over_base.get() for vocab in self.counterpart().unexcluded_vocabs])

    def is_valid_candidate(self) -> bool:
        return super().is_valid_candidate() and self.form not in self.surface_preferred_over_bases

    def counterpart(self) -> CandidateForm: return non_optional(self.candidate().surface)
