from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatching
    from sysutils.weak_ref import WeakRef

class Match(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, candidate: WeakRef[CandidateWordVariant], rules: VocabNoteMatching | None) -> None:
        self.candidate: WeakRef[CandidateWordVariant] = candidate
        self.parsed_form: str = candidate().form
        self.vocab_form: str = ""
        self.answer: str = ""
        self.readings: list[str] = []
        self.rules = rules
        self.is_configured_hidden = candidate().configuration.hidden_matches.excludes_at_index(self.parsed_form, candidate().start_index)
        self.is_configured_incorrect = candidate().configuration.incorrect_matches.excludes_at_index(self.parsed_form, candidate().start_index)

    @property
    def is_valid(self) -> bool:
        return not self.is_configured_incorrect

    @property
    def is_displayed(self) -> bool: return (self.is_valid_for_display
                                            or self._emergency_displayed)

    @property
    def is_valid_for_display(self) -> bool:
        return self.is_valid and not self.is_configured_hidden

    @property
    def _emergency_displayed(self) -> bool:
        return (self._must_include_some_variant
                and self._is_surface
                and not self._base_is_valid_word)

    @property
    def _base_is_valid_word(self) -> bool:
        base = self.candidate().candidate_word().base
        return base is not None and base.is_valid_candidate

    @property
    def _is_surface(self) -> bool: return self.candidate().is_surface
    @property
    def _must_include_some_variant(self) -> bool: return self.candidate().candidate_word().must_include_some_variant()

    @property
    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(self.is_configured_incorrect, "configured_incorrect")
                .append_if(self.is_configured_hidden, "configured_hidden")
                .as_set())
