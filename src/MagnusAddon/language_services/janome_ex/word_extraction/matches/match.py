from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.forbids_state import Forbids
from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_hidden import IsConfiguredHidden
from language_services.janome_ex.word_extraction.matches.state_tests.is_configured_incorrect import IsConfiguredIncorrect
from language_services.janome_ex.word_extraction.matches.state_tests.is_godan_imperative_surface_with_base import IsGodanImperativeInflectionWithBase
from language_services.janome_ex.word_extraction.matches.state_tests.is_godan_potential_surface_with_base import IsGodanPotentialInflectionWithBase
from language_services.janome_ex.word_extraction.matches.state_tests.is_inflected_surface_with_valid_base import IsInflectedSurfaceWithValidBase
from language_services.janome_ex.word_extraction.matches.state_tests.is_shadowed import IsShadowed
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class Match(WeakRefable, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant],
                 validity_requirements: list[MatchRequirement],
                 display_requirements: list[MatchRequirement]) -> None:
        weakref_self = WeakRef(self)
        self._is_not_shadowed_requirement: MatchRequirement = Forbids(IsShadowed(weakref_self))
        self._preliminarily_valid_for_display_requirement: MatchRequirement = Forbids(IsConfiguredHidden(weakref_self))
        self.weakref: WeakRef[Match] = weakref_self
        self._variant: WeakRef[CandidateWordVariant] = word_variant
        self._validity_requirements: list[MatchRequirement] = ([
                                                                       Forbids(IsConfiguredIncorrect(weakref_self)),
                                                                       Forbids(IsGodanPotentialInflectionWithBase(weakref_self)),
                                                                       Forbids(IsGodanImperativeInflectionWithBase(weakref_self)),
                                                                       Forbids(IsInflectedSurfaceWithValidBase(weakref_self)),
                                                               ]
                                                               + validity_requirements)
        self._display_requirements: list[MatchRequirement] = ([
                                                                      self._is_not_shadowed_requirement,
                                                                      self._preliminarily_valid_for_display_requirement
                                                              ]
                                                              + display_requirements)
        self._is_valid: bool | None = None

    @property
    def would_yield_to_upcoming_overlapping_compound(self) -> bool: return False

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
    def word(self) -> CandidateWord: return self.variant.word
    @property
    def variant(self) -> CandidateWordVariant: return self._variant()
    @property
    def is_preliminarily_valid_for_display(self) -> bool: return self._preliminarily_valid_for_display_requirement.is_fulfilled

    @property
    def is_valid(self) -> bool: return (self._is_valid_internal
                                        or (self.is_highlighted
                                            and not any(valid_sibling for valid_sibling in self._sibling_matches if valid_sibling._is_valid_internal)))
    @property
    def _is_valid_internal(self) -> bool:
        if self._is_valid is None:
            self._is_valid = self.__is_valid_internal_implementation()
        return self._is_valid

    def __is_valid_internal_implementation(self) -> bool: return all(requirement.is_fulfilled for requirement in self._validity_requirements)
    @property
    def is_highlighted(self) -> bool: return self.match_form in self.variant.configuration.highlighted_words
    @property
    def is_displayed(self) -> bool: return self.is_valid_for_display or self.is_emergency_displayed
    @property
    def start_index(self) -> int: return self.variant.start_index
    @property
    def is_valid_for_display(self) -> bool: return self.is_valid and all(requirement.is_fulfilled for requirement in self._display_requirements)

    @property
    def is_emergency_displayed(self) -> bool:
        return (self._surface_is_seemingly_valid_single_token
                and self.variant.is_surface
                and self._is_not_shadowed_requirement.is_fulfilled
                and not self._base_is_valid_word
                and not self._has_valid_for_display_sibling)

    @property
    def _has_valid_for_display_sibling(self) -> bool: return any(other_match for other_match in self._sibling_matches if other_match.is_valid_for_display)
    @property
    def _sibling_matches(self) -> list[Match]: return [match for match in self.variant.matches if match != self]
    @property
    def _base_is_valid_word(self) -> bool: return self.word.base_variant is not None and self.word.base_variant.has_valid_match

    @property
    def _surface_is_seemingly_valid_single_token(self) -> bool: return self.word.has_seemingly_valid_single_token

    @property
    def is_shadowed(self) -> bool: return self.word.is_shadowed
    @property
    def failure_reasons(self) -> list[str]: return [] if self.is_valid else [requirement.failure_reason for requirement in self._validity_requirements if not requirement.is_fulfilled]
    @property
    def hiding_reasons(self) -> list[str]: return [requirement.failure_reason for requirement in self._display_requirements if not requirement.is_fulfilled]

    @override
    def __repr__(self) -> str: return f"""{self.parsed_form}, {self.match_form[:10]}: failure_reasons: {" ".join(self.failure_reasons) or "None"} ## hiding_reasons: {" ".join(self.hiding_reasons) or "None"}"""

    @override
    def __str__(self) -> str: return self.__repr__()
