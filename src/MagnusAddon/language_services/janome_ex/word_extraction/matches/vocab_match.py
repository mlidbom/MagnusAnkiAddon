from __future__ import annotations

from typing import TYPE_CHECKING, final, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.match import Match
from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
from language_services.janome_ex.word_extraction.matches.state_tests.another_match_owns_the_form import ForbidsAnotherMatchIsHigherPriority
from language_services.janome_ex.word_extraction.matches.state_tests.forbids_compositionally_transparent_compound import ForbidsCompositionallyTransparentCompound
from language_services.janome_ex.word_extraction.matches.state_tests.forbids_yields_to_surface import ForbidsYieldsToSurface
from language_services.janome_ex.word_extraction.matches.state_tests.head.generic_forbids import Forbids
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_godan_imperative_prefix import RequiresOrForbidsHasGodanImperativePrefix
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_past_tense_stem import RequiresOrForbidsHasPastTenseStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.has_te_form_stem import RequiresOrForbidsHasTeFormStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.is_sentence_start import RequiresOrForbidsIsSentenceStart
from language_services.janome_ex.word_extraction.matches.state_tests.head.prefix_is_in import ForbidsPrefixIsIn, RequiresPrefixIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_forbids_adverb_stem import RequiresOrForbidsPrecedingAdverb
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_forbids_masu_stem import RequiresOrForbidsMasuStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_or_forbids_dictionary_form_prefix import RequiresOrForbidsDictionaryFormPrefix
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_or_forbids_dictionary_form_stem import RequiresOrForbidsDictionaryFormStem
from language_services.janome_ex.word_extraction.matches.state_tests.head.requires_or_forbids_generic import RequiresOrForbids
from language_services.janome_ex.word_extraction.matches.state_tests.is_exact_match import RequiresOrForbidsSurface
from language_services.janome_ex.word_extraction.matches.state_tests.is_ichidan_imperative import RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection
from language_services.janome_ex.word_extraction.matches.state_tests.is_poison_word import ForbidsIsPoisonWord
from language_services.janome_ex.word_extraction.matches.state_tests.is_single_token import RequiresOrForbidsIsSingleToken
from language_services.janome_ex.word_extraction.matches.state_tests.starts_with_godan_imperative_stem_or_inflection import RequiresOrForbidsStartsWithGodanImperativeStemOrInflection
from language_services.janome_ex.word_extraction.matches.state_tests.starts_with_godan_potential_stem_or_inflection import RequiresOrForbidsStartsWithGodanPotentialStemOrInflection
from language_services.janome_ex.word_extraction.matches.state_tests.surface_is_in import ForbidsSurfaceIsIn
from language_services.janome_ex.word_extraction.matches.state_tests.tail.forbids_has_displayed_overlapping_following_compound import ForbidsHasDisplayedOverlappingFollowingCompound
from language_services.janome_ex.word_extraction.matches.state_tests.tail.is_sentence_end import RequiresOrForbidsIsSentenceEnd
from language_services.janome_ex.word_extraction.matches.state_tests.tail.suffix_is_in import ForbidsSuffixIsIn
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from collections.abc import Callable

    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

@final
class VocabMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        self.weakref_vocab: WeakRef[VocabMatch] = WeakRef(self)
        self.vocab_inspector = VocabMatchInspector(self.weakref_vocab)
        self.requires_forbids = vocab.matching_configuration.requires_forbids
        self.rules = vocab.matching_configuration.configurable_rules
        self.vocab: VocabNote = vocab
        self._variant: WeakRef[CandidateWordVariant] = word_variant
        self._another_match_owns_the_form_cache: bool | None = None
        super().__init__(word_variant)

    _vocab_static_display_requirements_list: list[Callable[[VocabMatchInspector], FailedMatchRequirement | None]] = [
            ForbidsCompositionallyTransparentCompound.apply_to
    ]

    _vocab_static_display_requirements_list_combined: list[Callable[[VocabMatchInspector], FailedMatchRequirement | None]] = _vocab_static_display_requirements_list + Match._match_static_display_requirements

    @override
    def _create_static_display_requinement_failures(self) -> list[FailedMatchRequirement]:
        inspector = self.vocab_inspector
        return [failure for failure in (requirement(inspector) for requirement in VocabMatch._vocab_static_display_requirements_list_combined) if failure is not None]

    @override
    def _static_display_requirements_fulfilled(self) -> bool:
        inspector = self.vocab_inspector
        return not any(failure for failure in (requirement(inspector) for requirement in VocabMatch._vocab_static_display_requirements_list_combined) if failure is not None)

    @override
    def _create_dynamic_display_requirements(self) -> tuple[MatchRequirement | None, ...]:
        return (
                ForbidsHasDisplayedOverlappingFollowingCompound.apply_to(self.vocab_inspector, self.requires_forbids.yield_last_token.is_required),
        )

    _requirements_list: list[Callable[[VocabMatchInspector], FailedMatchRequirement | None]] = [
            # new style
            RequiresOrForbids("irrealis", lambda it: it.requires_forbids.irrealis, lambda it: it.previous_location_is_irrealis).apply_to,
            RequiresOrForbids("godan", lambda it: it.requires_forbids.godan, lambda it: it.previous_location_is_godan).apply_to,
            RequiresOrForbids("ichidan", lambda it: it.requires_forbids.ichidan, lambda it: it.previous_location_is_ichidan).apply_to,

            Forbids("compound_ending_on_dictionary_form_where_surface_differs_from_base", lambda it: it.is_compound_ending_on_dictionary_form_where_surface_differs_from_base).apply_to,

            # head requirements
            ForbidsPrefixIsIn.apply_to,
            RequiresPrefixIsIn.apply_to,
            RequiresOrForbidsIsSentenceStart.apply_to,
            RequiresOrForbidsHasTeFormStem.apply_to,
            RequiresOrForbidsHasPastTenseStem.apply_to,

            RequiresOrForbidsHasGodanImperativePrefix.apply_to,
            RequiresOrForbidsStartsWithGodanPotentialStemOrInflection.apply_to,
            RequiresOrForbidsStartsWithGodanImperativeStemOrInflection.apply_to,
            RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection.apply_to,

            # tail requirements
            RequiresOrForbidsIsSentenceEnd.apply_to,
            ForbidsSuffixIsIn.apply_to,

            # misc requirements
            ForbidsIsPoisonWord.apply_to,
            RequiresOrForbidsMasuStem.apply_to,
            RequiresOrForbidsPrecedingAdverb.apply_to,
            RequiresOrForbidsDictionaryFormStem.apply_to,
            RequiresOrForbidsDictionaryFormPrefix.apply_to,

            RequiresOrForbidsSurface.apply_to,
            RequiresOrForbidsIsSingleToken.apply_to,
            ForbidsSurfaceIsIn.apply_to,
            ForbidsYieldsToSurface.apply_to,  # todo this should be in display requirements right?
    ]

    _combined_requirements: list[Callable[[VocabMatchInspector], FailedMatchRequirement | None]] = Match._match_primary_validity_requirements + _requirements_list

    @override
    def _create_primary_validity_failures(self) -> list[FailedMatchRequirement]:
        inspector = self.vocab_inspector
        return [failure for failure in (requirement(inspector) for requirement in VocabMatch._combined_requirements) if failure is not None]

    @override
    def _is_primarily_valid(self) -> bool:
        inspector = self.vocab_inspector
        return not any(failure for failure in (requirement(inspector) for requirement in VocabMatch._combined_requirements) if failure is not None)

    @override
    def _create_interdependent_validity_failures(self) -> list[FailedMatchRequirement]:
        failure = ForbidsAnotherMatchIsHigherPriority.apply_to(self.vocab_inspector)
        return [failure] if failure is not None else []

    @override
    def _is_interdepentently_valid(self) -> bool:
        return ForbidsAnotherMatchIsHigherPriority.apply_to(self.vocab_inspector) is None

    @property
    def matching_configuration(self) -> VocabNoteMatchingConfiguration: return self.vocab.matching_configuration
    @property
    @override
    def match_form(self) -> str: return self.vocab.get_question()
    @property
    @override
    def answer(self) -> str: return self.vocab.get_answer()
    @property
    @override
    def readings(self) -> list[str]: return self.vocab.readings.get()

    @property
    @override
    def parsed_form(self) -> str:
        return self.vocab.question.raw \
            if self.matching_configuration.bool_flags.question_overrides_form.is_set() \
            else super().parsed_form

    @property
    @override
    def exclusion_form(self) -> str:
        question = self.vocab.question
        tokenized_form = super().tokenized_form
        if question.raw == tokenized_form and question.is_disambiguated:
            return question.disambiguation_name
        return question.raw

    @property
    def another_match_is_higher_priority(self) -> bool:
        if self._another_match_owns_the_form_cache is None:
            if any(other_match for other_match in self.variant.vocab_matches  # noqa: SIM103
                   if other_match != self
                      and other_match.is_primarily_valid
                      and other_match._is_higher_priority_for_match(self)):
                self._another_match_owns_the_form_cache = True
            else:
                self._another_match_owns_the_form_cache = False

        return self._another_match_owns_the_form_cache

    def _is_higher_priority_for_match(self, other: VocabMatch) -> bool:
        owns_form = self.vocab.forms.is_owned_form(self.tokenized_form)
        other_owns_form = other.vocab.forms.is_owned_form(self.tokenized_form)
        if owns_form and not other_owns_form:  # noqa: SIM103
            return True
        if not owns_form and other_owns_form:
            return False
        if self.vocab.matching_configuration.custom_requirements_weight > other.matching_configuration.custom_requirements_weight:  # noqa: SIM103
            return True
        return False

    @override
    def _start_index(self) -> int:
        if self.matching_configuration.bool_flags.question_overrides_form.is_set():
            length_diff = (len(self.vocab.get_question()) - len(self.tokenized_form))
            if length_diff != 0 and self.tokenized_form in self.vocab.get_question():  # we often "steal" characters backwards, forwards is not supported so this should be sufficient, we don't need all the complexity below
                return super()._start_index() - length_diff
            # if self.requires_forbids.a_stem.is_required or self.requires_forbids.e_stem.is_required:
            #     return super()._start_index() - 1
            # if self.rules.required_prefix.any():
            #     matched_prefixes = [prefix for prefix in self.rules.required_prefix.get()
            #                         if self.parsed_form.startswith(prefix)]
            #     if matched_prefixes:
            #         matched_prefix_length = max(len(prefix) for prefix in matched_prefixes)
            #         return super()._start_index() - matched_prefix_length

        return super()._start_index()

    @override
    def __repr__(self) -> str: return f"""{self.vocab.get_question()}, {self.vocab.get_answer()[:10]}: {self.match_form[:10]}: failure_reasons: {" ".join(self.failure_reasons) or "None"} ## hiding_reasons: {" ".join(self.hiding_reasons) or "None"}"""
