from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatching
    from sysutils.weak_ref import WeakRef

class Match(WeakRefable, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], rules: VocabNoteMatching | None) -> None:
        self.variant: WeakRef[CandidateWordVariant] = word_variant
        self.tokenized_form: str = word_variant().form
        self.parsed_form: str = self.tokenized_form
        self.match_form: str = self.tokenized_form
        self.answer: str = ""
        self.readings: list[str] = []
        self.rules = rules
        self.is_configured_hidden = word_variant().configuration.hidden_matches.excludes_at_index(self.tokenized_form, word_variant().start_index)
        self.is_configured_incorrect = word_variant().configuration.incorrect_matches.excludes_at_index(self.tokenized_form, word_variant().start_index)

    @property
    def is_valid(self) -> bool:
        return self._is_valid_internal or self.is_highlighted

    @property
    def surface_form(self) -> str: return self.variant().word().surface.form

    @property
    def _is_valid_internal(self) -> bool:
        return not self.is_configured_incorrect

    @property
    def is_highlighted(self) -> bool: return self.match_form in self.variant().configuration.highlighted_words

    @property
    def is_secondary_match(self) -> bool: raise NotImplementedError()

    @property
    def is_displayed(self) -> bool: return (self.is_valid_for_display
                                            or self.is_emergency_displayed)

    @property
    def start_index(self) -> int: return self.variant().start_index

    @property
    def is_indexed(self) -> bool: return self.is_valid or self.is_emergency_displayed

    @property
    def is_valid_for_display(self) -> bool:
        return self.is_valid and not self.is_configured_hidden and not self.is_shadowed

    @property
    def is_emergency_displayed(self) -> bool:
        return (self.surface_is_seemingly_valid_single_token
                and self.variant().is_surface
                and not self._base_is_valid_word
                and not any(other_match for other_match in self.variant().matches if other_match.is_valid_for_display))

    @property
    def _has_valid_for_display_sibling(self) -> bool: return any(other_match for other_match in self._sibling_matches if other_match.is_valid_for_display)
    @property
    def _sibling_matches(self) -> list[Match]: return [match for match in self.variant().matches if match != self]
    @property
    def _base_is_valid_word(self) -> bool:
        base = self.variant().word().base
        return base is not None and base.is_valid_candidate

    @property
    def word(self) -> CandidateWord: return self.variant().word()
    @property
    def surface_is_seemingly_valid_single_token(self) -> bool: return self.variant().word().surface_is_seemingly_valid_single_token()

    @property
    def is_shadowed(self) -> bool: return self.variant().is_shadowed

    @property
    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_incorrect, "configured_incorrect")
                .as_set())

    @property
    def hiding_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_hidden, "configured_hidden")
                .append_if_lambda(self.is_shadowed, lambda: f"shadowed_by:{self.variant().shadowed_by_text}")
                .as_set())

    def __repr__(self) -> str: return f"""{self.parsed_form}, {self.match_form[:10]}: {" ".join(self.failure_reasons)} {" ".join(self.hiding_reasons)}"""
