from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class DisplayRequirements(Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        vocab = match().vocab
        self.rules = vocab.matching_configuration
        self.match = match

        self.is_yield_last_token_to_overlapping_compound_requirement_fulfilled = self._is_yield_last_token_to_overlapping_compound_requirement_fulfilled()

        # if we have matches that owns the form, it calls the shots for display, no other matches are allowed to be displayed
        self.yields_to_form_owning_match: bool = match().is_secondary_match

        self.are_fulfilled = (self.is_yield_last_token_to_overlapping_compound_requirement_fulfilled
                              and not self.yields_to_form_owning_match)

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if_lambda(not self.is_yield_last_token_to_overlapping_compound_requirement_fulfilled, lambda: f"yield_last_token_to_overlapping_compound:{self.match().word_variant().word.end_location.display_words[0].display_variants[0].form}")
                .append_if(self.yields_to_form_owning_match, "yields_to_form_owning_match")
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())

    def _is_yield_last_token_to_overlapping_compound_requirement_fulfilled(self) -> bool:
        if not self.rules.flags.yield_last_token.is_required: return True

        #todo: this is a problematic reference to display_words_starting_here. Thot collection is initialized using this class,
        # so this class will return different results depending on whether it is used after or before display_words_starting_here is first initialized. Ouch
        last_token_display_words: list[CandidateWord] = self.match().word_variant().word.end_location.display_words
        if not last_token_display_words: return True

        return not last_token_display_words[0].is_custom_compound
