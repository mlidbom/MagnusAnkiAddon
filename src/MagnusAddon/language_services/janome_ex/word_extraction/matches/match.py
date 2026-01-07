from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
from language_services.janome_ex.word_extraction.matches.state_tests.forbids_compounds import ForbidsConfiguredToHideCompounds
from language_services.janome_ex.word_extraction.matches.state_tests.forbids_dictionary_form_verb_inflection import ForbidsDictionaryInflectionSurfaceWithBase
from language_services.janome_ex.word_extraction.matches.state_tests.forbids_dictionary_form_verb_stem_surface_as_compound_end import ForbidsDictionaryVerbFormStemAsCompoundEnd
from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_hidden import ForbidsIsConfiguredHidden
from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_incorrect import ForbidsIsConfiguredIncorrect
from language_services.janome_ex.word_extraction.matches.state_tests.is_godan_imperative_surface_with_base import ForbidsIsGodanImperativeInflectionWithBase
from language_services.janome_ex.word_extraction.matches.state_tests.is_godan_potential_surface_with_base import ForbidsIsGodanPotentialInflectionWithBase
from language_services.janome_ex.word_extraction.matches.state_tests.is_inflected_surface_with_valid_base import ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb
from language_services.janome_ex.word_extraction.matches.state_tests.is_shadowed import ForbidsIsShadowed
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

class Match(WeakRefable, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant]) -> None:
        weakref_self = WeakRef(self)
        inspector = MatchInspector(weakref_self)
        self.inspector: MatchInspector = inspector
        self.weakref: WeakRef[Match] = weakref_self
        self._variant: WeakRef[CandidateWordVariant] = word_variant

        self._is_primarily_valid_internal_cache: bool | None = None
        self._is_valid_internal_cache: bool | None = None
        self._is_valid_cache: bool | None = None
        self._start_index_cache: int | None = None

        self._primary_validity_failures_cache: list[FailedMatchRequirement] | None = None
        self._interdependent_validity_failures_cache: list[FailedMatchRequirement] | None = None
        self._display_requirements_cache: list[MatchRequirement] | None = None

    @property
    def _primary_validity_failures(self) -> list[FailedMatchRequirement]:
        if self._primary_validity_failures_cache is None:
            self._primary_validity_failures_cache = [r for r in (
                    ForbidsIsConfiguredIncorrect.apply_to(self.inspector),
                    ForbidsDictionaryInflectionSurfaceWithBase.apply_to(self.inspector),
                    ForbidsDictionaryVerbFormStemAsCompoundEnd.apply_to(self.inspector),
                    ForbidsIsGodanPotentialInflectionWithBase.apply_to(self.inspector),
                    ForbidsIsGodanImperativeInflectionWithBase.apply_to(self.inspector),
                    ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb.apply_to(self.inspector),
                    *self._create_primary_validity_failures()
            ) if r is not None]
        return self._primary_validity_failures_cache

    @property
    def _interdependent_validity_failures(self) -> list[FailedMatchRequirement]:
        if self._interdependent_validity_failures_cache is None:
            self._interdependent_validity_failures_cache = [r for r in self._create_interdependent_validity_failures() if r is not None]
        return self._interdependent_validity_failures_cache

    @property
    def _display_requirements(self) -> list[MatchRequirement]:
        if self._display_requirements_cache is None:
            self._display_requirements_cache = [r for r in (
                    ForbidsIsShadowed(self.inspector),
                    ForbidsIsConfiguredHidden.apply_to(self.inspector),
                    ForbidsConfiguredToHideCompounds.apply_to(self),
                    *self._create_display_requirements()) if r is not None]
        return self._display_requirements_cache

    def _create_primary_validity_failures(self) -> list[FailedMatchRequirement | None]: return []
    def _create_interdependent_validity_failures(self) -> tuple[FailedMatchRequirement | None, ...]: return ()
    def _create_display_requirements(self) -> tuple[MatchRequirement | None, ...]: return ()

    @property
    def answer(self) -> str: raise NotImplementedError()
    @property
    def readings(self) -> list[str]: raise NotImplementedError()

    @property
    def tokenized_form(self) -> str: return self.variant.form
    @property
    def match_form(self) -> str: return self.tokenized_form
    @property
    def parsed_form(self) -> str: return self.tokenized_form
    @property
    def exclusion_form(self) -> str: return self.variant.form

    @property
    def word(self) -> CandidateWord: return self.variant.word
    @property
    def variant(self) -> CandidateWordVariant: return self._variant()

    @property
    def is_valid(self) -> bool:
        if self._is_valid_cache is None:
            self._is_valid_cache = self._is_valid()

        return self._is_valid_cache

    def _is_valid(self) -> bool:
        return self._is_valid_internal or self.is_highlighted

    @property
    def is_primarily_valid(self) -> bool:
        if self._is_primarily_valid_internal_cache is None:
            self._is_primarily_valid_internal_cache = not self._primary_validity_failures
        return self._is_primarily_valid_internal_cache

    @property
    def _is_valid_internal(self) -> bool:
        if self._is_valid_internal_cache is None:
            self._is_valid_internal_cache = self.is_primarily_valid and not self._interdependent_validity_failures
        return self._is_valid_internal_cache

    @property
    def is_highlighted(self) -> bool: return self.exclusion_form in self.variant.configuration.highlighted_words
    @property
    def is_displayed(self) -> bool: return self.is_valid_for_display or self._is_emergency_displayed

    @property
    def start_index(self) -> int:
        if self._start_index_cache is not None:
            return self._start_index_cache
        self._start_index_cache = self._start_index()
        return self.variant.start_index

    def _start_index(self) -> int: return self.variant.start_index
    @property
    def is_valid_for_display(self) -> bool: return self.is_valid and all(requirement.is_fulfilled for requirement in self._display_requirements)

    @property
    def _is_emergency_displayed(self) -> bool:
        return (self.variant.is_surface
                and self._surface_is_seemingly_valid_single_token
                and not self._base_is_valid_word
                and not self.is_shadowed
                and not self._has_valid_for_display_sibling)

    @property
    def _has_valid_for_display_sibling(self) -> bool: return any(other_match for other_match in self.variant.matches if other_match != self and other_match.is_valid_for_display)
    @property
    def _base_is_valid_word(self) -> bool: return self.word.base_variant is not None and self.word.base_variant.has_valid_match
    @property
    def _surface_is_seemingly_valid_single_token(self) -> bool: return self.word.has_seemingly_valid_single_token
    @property
    def is_shadowed(self) -> bool: return self.word.is_shadowed
    @property
    def failure_reasons(self) -> list[str]: return [] if self.is_valid else ([requirement.failure_reason for requirement in self._primary_validity_failures]
                                                                             + [requirement.failure_reason for requirement in self._interdependent_validity_failures])
    @property
    def hiding_reasons(self) -> list[str]: return [requirement.failure_reason for requirement in self._display_requirements if not requirement.is_fulfilled]

    def to_exclusion(self) -> WordExclusion: return WordExclusion.at_index(self.exclusion_form, self.start_index)

    @override
    def __repr__(self) -> str: return f"""{self.parsed_form}, {self.match_form[:10]}: failure_reasons: {" ".join(self.failure_reasons) or "None"} ## hiding_reasons: {" ".join(self.hiding_reasons) or "None"}"""

    @override
    def __str__(self) -> str: return self.__repr__()
