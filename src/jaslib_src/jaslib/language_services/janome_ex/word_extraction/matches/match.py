# from __future__ import annotations
#
# from typing import TYPE_CHECKING, override
#
# from autoslot import Slots
# from jaspythonutils.sysutils.abstract_method_called_error import AbstractMethodCalledError
# from jaspythonutils.sysutils.weak_ref import WeakRef, WeakRefable
#
# from jaslib.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.forbids_compounds import ForbidsConfiguredToHideAllCompounds
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.forbids_dictionary_form_verb_inflection import ForbidsDictionaryInflectionSurfaceWithBase
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.forbids_dictionary_form_verb_stem_surface_as_compound_end import ForbidsDictionaryVerbFormStemAsCompoundEnd
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.generic_forbids import Forbids
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.is_configured_hidden import ForbidsIsConfiguredHidden
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.is_configured_incorrect import ForbidsIsConfiguredIncorrect
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.is_godan_imperative_surface_with_base import ForbidsIsGodanImperativeInflectionWithBase
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.is_godan_potential_surface_with_base import ForbidsIsGodanPotentialInflectionWithBase
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.is_inflected_surface_with_valid_base import ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb
# from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.is_shadowed import ForbidsIsShadowed
# from jaslib.language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
#
# if TYPE_CHECKING:
#     from collections.abc import Callable
#
#     from jaslib.language_services.janome_ex.word_extraction.candidate_word import CandidateWord
#     from jaslib.language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
#     from jaslib.language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
#     from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
#
# class Match(WeakRefable, Slots):
#     _match_primary_validity_requirements: list[Callable[[MatchInspector], FailedMatchRequirement | None]] = [
#             ForbidsIsConfiguredIncorrect.apply_to,
#             ForbidsDictionaryInflectionSurfaceWithBase.apply_to,
#             ForbidsDictionaryVerbFormStemAsCompoundEnd.apply_to,
#             ForbidsIsGodanPotentialInflectionWithBase.apply_to,
#             ForbidsIsGodanImperativeInflectionWithBase.apply_to,
#             ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb.apply_to,
#             Forbids("compound_ending_on_dictionary_form_where_surface_differs_from_base", lambda it: it.is_compound_ending_on_dictionary_form_where_surface_differs_from_base).apply_to,
#     ]
#
#     _match_static_display_requirements: list[Callable[[MatchInspector], FailedMatchRequirement | None]] = [
#             ForbidsIsConfiguredHidden.apply_to,
#             ForbidsConfiguredToHideAllCompounds.apply_to
#     ]
#
#     def __init__(self, word_variant: WeakRef[CandidateWordVariant]) -> None:
#         weakref_self = WeakRef(self)
#         inspector = MatchInspector(weakref_self)
#         self.inspector: MatchInspector = inspector
#         self.weakref: WeakRef[Match] = weakref_self
#         self._variant: WeakRef[CandidateWordVariant] = word_variant
#
#         self._is_primarily_valid_internal_cache: bool | None = None
#         self._is_valid_internal_cache: bool | None = None
#         self._is_valid_cache: bool | None = None
#         self._start_index_cache: int | None = None
#         self._static_display_requirements_fulfilled_cache: bool | None = None
#
#         self._display_requirements_cache: list[MatchRequirement] | None = None
#
#     @property
#     def _dynamic_display_requirements(self) -> list[MatchRequirement]:
#         if self._display_requirements_cache is None:
#             self._display_requirements_cache = [r for r in (
#                     ForbidsIsShadowed(self.inspector),
#                     *self._create_dynamic_display_requirements()) if r is not None]
#         return self._display_requirements_cache
#
#     def _create_primary_validity_failures(self) -> list[FailedMatchRequirement]:
#         inspector = self.inspector
#         return [failure for failure in (requirement(inspector) for requirement in self._match_primary_validity_requirements) if failure is not None]
#
#     def _is_primarily_valid(self) -> bool:
#         inspector = self.inspector
#         return not any(failure for failure in (requirement(inspector) for requirement in self._match_primary_validity_requirements) if failure is not None)
#
#     def _is_interdepentently_valid(self) -> bool: return True
#
#     def _create_interdependent_validity_failures(self) -> list[FailedMatchRequirement]: return []
#     def _create_static_display_requinement_failures(self) -> list[FailedMatchRequirement]:
#         inspector = self.inspector
#         return [failure for failure in (requirement(inspector) for requirement in self._match_static_display_requirements) if failure is not None]
#
#     @property
#     def static_display_requirements_fulfilled(self) -> bool:
#         if self._static_display_requirements_fulfilled_cache is None:
#             self._static_display_requirements_fulfilled_cache = self._static_display_requirements_fulfilled()
#         return self._static_display_requirements_fulfilled_cache
#
#     def _static_display_requirements_fulfilled(self) -> bool:
#         inspector = self.inspector
#         return not any(failure for failure in (requirement(inspector) for requirement in self._match_static_display_requirements) if failure is not None)
#
#     def _create_dynamic_display_requirements(self) -> tuple[MatchRequirement | None, ...]: return ()
#
#     @property
#     def answer(self) -> str: raise AbstractMethodCalledError()
#     @property
#     def readings(self) -> list[str]: raise AbstractMethodCalledError()
#     @property
#     def tokenized_form(self) -> str: return self.variant.form
#     @property
#     def match_form(self) -> str: return self.tokenized_form
#     @property
#     def parsed_form(self) -> str: return self.tokenized_form
#     @property
#     def exclusion_form(self) -> str: return self.variant.form
#
#     @property
#     def word(self) -> CandidateWord: return self.variant.word
#     @property
#     def variant(self) -> CandidateWordVariant: return self._variant()
#
#     @property
#     def is_valid(self) -> bool:
#         if self._is_valid_cache is None:
#             self._is_valid_cache = self._is_valid()
#         return self._is_valid_cache
#
#     def _is_valid(self) -> bool:
#         return self._is_valid_internal or self.is_highlighted
#
#     @property
#     def is_primarily_valid(self) -> bool:
#         if self._is_primarily_valid_internal_cache is None:
#             self._is_primarily_valid_internal_cache = self._is_primarily_valid()
#         return self._is_primarily_valid_internal_cache
#
#     @property
#     def _is_valid_internal(self) -> bool:
#         if self._is_valid_internal_cache is None:
#             self._is_valid_internal_cache = self.is_primarily_valid and self._is_interdepentently_valid()
#         return self._is_valid_internal_cache
#
#     @property
#     def is_highlighted(self) -> bool: return self.exclusion_form in self.variant.configuration.highlighted_words
#     @property
#     def is_displayed(self) -> bool: return self.is_valid_for_display or self.is_emergency_displayed
#
#     @property
#     def start_index(self) -> int:
#         if self._start_index_cache is None:
#             self._start_index_cache = self._start_index()
#         return self._start_index_cache
#
#     def _start_index(self) -> int: return self.variant.start_index
#     @property
#     def is_valid_for_display(self) -> bool: return self.is_valid and self.static_display_requirements_fulfilled and all(requirement.is_fulfilled for requirement in self._dynamic_display_requirements)
#
#     @property
#     def is_emergency_displayed(self) -> bool:
#         return not self.is_valid and (self.variant.is_surface
#                                       and self._surface_is_seemingly_valid_single_token
#                                       and not self._base_is_valid_word
#                                       and not self.is_shadowed
#                                       and not self._has_valid_for_display_sibling)
#
#     @property
#     def _has_valid_for_display_sibling(self) -> bool: return any(other_match for other_match in self.variant.matches if other_match != self and other_match.is_valid_for_display)
#     @property
#     def _base_is_valid_word(self) -> bool: return self.word.base_variant is not None and self.word.base_variant.has_valid_match
#     @property
#     def _surface_is_seemingly_valid_single_token(self) -> bool: return self.word.has_seemingly_valid_single_token
#     @property
#     def is_shadowed(self) -> bool: return self.word.is_shadowed
#     @property
#     def failure_reasons(self) -> list[str]: return [] if self.is_valid else ([requirement.failure_reason for requirement in self._create_primary_validity_failures()]
#                                                                              + [requirement.failure_reason for requirement in self._create_interdependent_validity_failures()])
#     @property
#     def hiding_reasons(self) -> list[str]: return ([requirement.failure_reason for requirement in self._dynamic_display_requirements if not requirement.is_fulfilled] +
#                                                    [requirement.failure_reason for requirement in self._create_static_display_requinement_failures()])
#
#     # noinspection PyUnusedFunction
#     def to_exclusion(self) -> WordExclusion: return WordExclusion.at_index(self.exclusion_form, self.start_index)
#
#     @override
#     def __repr__(self) -> str: return f"""{self.parsed_form}, {self.match_form[:10]}: failure_reasons: {" ".join(self.failure_reasons) or "None"} ## hiding_reasons: {" ".join(self.hiding_reasons) or "None"}"""
#
#     @override
#     def __str__(self) -> str: return self.__repr__()
