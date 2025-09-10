from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatching
    from sysutils.weak_ref import WeakRef

class Match(WeakRefable, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], rules: VocabNoteMatching | None) -> None:
        self.start_index = word_variant().start_index
        self.word_variant: WeakRef[CandidateWordVariant] = word_variant
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
    def _is_valid_internal(self) -> bool:
        return not self.is_configured_incorrect

    @property
    def is_highlighted(self) -> bool: return self.match_form in self.word_variant().configuration.highlighted_words

    @property
    def is_secondary_match(self) -> bool: raise NotImplementedError()

    @property
    def is_displayed(self) -> bool: return (self.is_valid_for_display
                                            or self._emergency_displayed)

    @property
    def is_valid_for_display(self) -> bool:
        return self.is_valid and not self.is_configured_hidden and not self.is_shadowed

    @property
    def _emergency_displayed(self) -> bool:
        return (self._must_include_some_variant
                and self._is_surface
                and not self._base_is_valid_word
                and not any(other_match for other_match in self.word_variant().matches if other_match.is_valid_for_display))

    @property
    def _base_is_valid_word(self) -> bool:
        base = self.word_variant().word().base
        return base is not None and base.is_valid_candidate

    @property
    def _is_surface(self) -> bool: return self.word_variant().is_surface
    @property
    def _must_include_some_variant(self) -> bool: return self.word_variant().word().must_include_some_variant()

    @property
    def is_shadowed(self) -> bool: return self.word_variant().is_shadowed

    @property
    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_incorrect, "configured_incorrect")
                .as_set())

    @property
    def hiding_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_hidden, "configured_hidden")
                .append_if_lambda(self.is_shadowed, lambda: f"shadowed_by:{self.word_variant().shadowed_by_text}")
                .as_set())
