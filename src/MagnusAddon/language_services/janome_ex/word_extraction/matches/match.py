from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from sysutils.weak_ref import WeakRef

class Match(WeakRefable, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant],
                 validity_requirements: list[MatchRequirement],
                 display_requirements: list[MatchRequirement]) -> None:
        self._variant: WeakRef[CandidateWordVariant] = word_variant
        self._validity_requirements: list[MatchRequirement] = validity_requirements
        self._display_requirements: list[MatchRequirement] = display_requirements

    @property
    def answer(self) -> str: raise NotImplementedError()
    @property
    def readings(self) -> list[str]: raise NotImplementedError()
    @property
    def is_secondary_match(self) -> bool: raise NotImplementedError()

    @property
    def tokenized_form(self) -> str: return self.variant.form
    @property
    def match_form(self) -> str: return self.tokenized_form
    @property
    def parsed_form(self) -> str: return self.tokenized_form

    @property
    def is_configured_hidden(self) -> bool: return self.variant.configuration.hidden_matches.excludes_at_index(self.tokenized_form, self.variant.start_index)
    @property
    def is_configured_incorrect(self) -> bool: return self.variant.configuration.incorrect_matches.excludes_at_index(self.tokenized_form, self.variant.start_index)

    @property
    def word(self) -> CandidateWord: return self.variant.word
    @property
    def variant(self) -> CandidateWordVariant: return self._variant()

    @property
    def is_valid(self) -> bool: return self._is_valid_internal or self.is_highlighted
    @property
    def _is_valid_internal(self) -> bool: return not self.is_configured_incorrect
    @property
    def is_highlighted(self) -> bool: return self.match_form in self.variant.configuration.highlighted_words
    @property
    def is_displayed(self) -> bool: return self.is_valid_for_display or self.is_emergency_displayed
    @property
    def start_index(self) -> int: return self.variant.start_index
    @property
    def is_valid_for_display(self) -> bool: return self.is_valid and not self.is_configured_hidden and not self.is_shadowed

    @property
    def is_emergency_displayed(self) -> bool:
        return (self._surface_is_seemingly_valid_single_token
                and self.variant.is_surface
                and not self.is_shadowed
                and not self._base_is_valid_word
                and not self._has_valid_for_display_sibling)

    @property
    def _has_valid_for_display_sibling(self) -> bool: return any(other_match for other_match in self._sibling_matches if other_match.is_valid_for_display)
    @property
    def _sibling_matches(self) -> list[Match]: return [match for match in self.variant.matches if match != self]
    @property
    def _base_is_valid_word(self) -> bool: return self.word.base_variant is not None and self.word.base_variant.is_valid

    @property
    def _surface_is_seemingly_valid_single_token(self) -> bool: return self.word.has_seemingly_valid_single_token

    @property
    def is_shadowed(self) -> bool: return self.word.is_shadowed

    @property
    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_incorrect, "configured_incorrect")
                .as_set())

    @property
    def hiding_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_hidden, "configured_hidden")
                .append_if_lambda(self.is_shadowed, lambda: f"shadowed_by:{self.word.shadowed_by_text}")
                .as_set())

    @override
    def __repr__(self) -> str: return f"""{self.parsed_form}, {self.match_form[:10]}: {" ".join(self.failure_reasons)} {" ".join(self.hiding_reasons)}"""
