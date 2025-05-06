from __future__ import annotations
from typing import TYPE_CHECKING

from language_services import conjugator
from language_services.janome_ex.word_extraction.display_form import DisplayForm, MissingDisplayForm, VocabDisplayForm
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import Mine
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabnote import VocabNote

from sysutils.ex_str import newline

_noise_characters = {'.', ',', ':', ';', '/', '|', '。', '、'}
class CandidateForm:
    def __init__(self, candidate: CandidateWord, is_surface: bool, form: str):
        from ankiutils import app
        from language_services.jamdict_ex.dict_lookup import DictLookup

        self.start_index:int = candidate.locations[0].character_start_index
        self.configuration_exclusions:list[WordExclusion] = candidate.analysis.exclusions
        self.candidate:CandidateWord = candidate
        self.is_surface:bool = is_surface
        self.form:str = form

        self.dict_lookup: DictLookup = DictLookup.lookup_word_shallow(form)
        self.all_vocabs: list[VocabNote] = app.col().vocab.with_form(form)

        def is_excluded_form(form_: str) -> bool:
            return any(exclusion for exclusion in self.configuration_exclusions if exclusion.excludes_form_at_index(form_, self.start_index))

        self.unexcluded_vocabs: list[VocabNote] = [v for v in self.all_vocabs if not is_excluded_form(v.get_question())]
        self.excluded_vocabs: list[VocabNote] = [v for v in self.all_vocabs if is_excluded_form(v.get_question())]

        self.forms_excluded_by_vocab_configuration: set[str] = set().union(*[v.get_excluded_forms() for v in self.unexcluded_vocabs])

        self.is_word: bool = self.dict_lookup.found_words() or len(self.all_vocabs) > 0
        self.is_excluded_by_config: bool = is_excluded_form(form)
        self.is_self_excluded: bool = form in self.forms_excluded_by_vocab_configuration

        self.possible_contextual_exclusions = [excluded for excluded in self.forms_excluded_by_vocab_configuration if self.form in excluded]
        self.is_contextually_excluded: bool = self._is_contextually_excluded()

        self.forms_excluded_by_compound_root_vocab_configuration: set[str] = set()
        self.is_excluded_by_compound_root_vocab_configuration: bool = False
        self.exact_match_required_by_vocab_configuration: bool = any(v for v in self.unexcluded_vocabs if v.requires_exact_match())
        self.exact_match_required_by_counterpart_vocab_configuration:bool = False
        self.exact_match_required:bool = False
        self.exact_match_requirement_fulfilled: bool = False

        self.display_forms:list[DisplayForm] = []

    def _counterpart(self) -> CandidateForm: raise Exception("Not implemented")

    def complete_analysis(self) -> None:
        self.forms_excluded_by_compound_root_vocab_configuration = self.candidate.locations[0].all_candidates[-1].base.forms_excluded_by_vocab_configuration
        self.is_excluded_by_compound_root_vocab_configuration = self.form in self.forms_excluded_by_compound_root_vocab_configuration
        self.exact_match_required_by_counterpart_vocab_configuration = self._counterpart().exact_match_required_by_vocab_configuration
        self.exact_match_required = self.exact_match_required_by_vocab_configuration or self.exact_match_required_by_counterpart_vocab_configuration
        self.exact_match_requirement_fulfilled = self.form == self._counterpart().form or not self.exact_match_required

        if self.unexcluded_vocabs:
            self.display_forms = [VocabDisplayForm(self, voc) for voc in self.unexcluded_vocabs if self.vocab_is_matching(voc)]
            override_form = [df for df in self.display_forms if df.parsed_form != self.form]
            if any(override_form):
                self.form = override_form[0].parsed_form
        else:
            self.display_forms = [MissingDisplayForm(self)]

    def vocab_is_matching(self, vocab:VocabNote) -> bool:
        if vocab.has_tag(Mine.Tags.requires_a_stem):
            return self._previous_token_ends_on_a_stem()
        if vocab.has_tag(Mine.Tags.requires_e_stem):
            return self._previous_token_ends_on_e_stem()
        return True

    def _previous_token_ends_on_a_stem(self) -> bool:
        previous = self.candidate.start_location.previous
        if previous is not None:
            return previous.surface[-1] in conjugator.a_stem_characters
        return False

    def _previous_token_ends_on_e_stem(self) -> bool:
        previous = self.candidate.start_location.previous
        if previous is not None:
            return previous.surface[-1] in conjugator.e_stem_characters
        return False


    def is_valid_candidate(self) -> bool:
        return ((self.is_word or not self.candidate.is_custom_compound)
                and self.form not in _noise_characters
                and not self.is_excluded_by_config
                and not self.is_self_excluded
                and not self.is_contextually_excluded
                and not self.is_excluded_by_compound_root_vocab_configuration
                and self.exact_match_requirement_fulfilled)

    def _is_contextually_excluded(self) -> bool:
        for exclusion in self.possible_contextual_exclusions:
            if exclusion.endswith(self.form):
                previous_location = self.candidate.start_location.previous
                if previous_location is not None:
                    extended = previous_location.surface + self.form
                    if extended.endswith(self.form):
                        return True

            if exclusion.startswith(self.form):
                next_location = self.candidate.start_location.previous
                if next_location is not None:
                    extended = self.form + next_location.surface
                    if extended.startswith(self.form):
                        return True

        return False


    def __repr__(self) -> str:
        return f"""CandidateForm: {self.form}, ivc:{self.is_valid_candidate()}, iw:{self.is_word} ie:{self.is_excluded_by_config}""".replace(newline, "")

class SurfaceCandidateForm(CandidateForm):
    def __init__(self, candidate: CandidateWord):
        super().__init__(candidate, True, "".join([t.surface for t in candidate.locations]) + "")

    def _counterpart(self) -> CandidateForm: return non_optional(self.candidate.base)

class BaseCandidateForm(CandidateForm):
    def __init__(self, candidate: CandidateWord):
        base_form = "".join([t.surface for t in candidate.locations[:-1]]) + candidate.locations[-1].base
        if not candidate.is_custom_compound:
            base_form = candidate.locations[-1].token.base_form_for_non_compound_vocab_matching

        super().__init__(candidate, False, base_form)
        self.last_location_is_excluded_form:bool = False
        self.analysis_completed: bool = False


    def _counterpart(self) -> CandidateForm: return non_optional(self.candidate.surface)

    def complete_analysis(self) -> None:
        if self.analysis_completed: return
        self.analysis_completed = True

        super().complete_analysis()

        if self.candidate.is_custom_compound:
            last_location_shortest_candidate = self.candidate.end_location.all_candidates[-1]
            if not last_location_shortest_candidate.should_include_base:
                self.last_location_is_excluded_form = True

    def is_valid_candidate(self) -> bool:
        return super().is_valid_candidate() and not self.last_location_is_excluded_form