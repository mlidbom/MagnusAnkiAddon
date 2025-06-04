from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class DisplayRequirements(Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        vocab = match().vocab
        self.rules = vocab.matching_rules
        self.match = match

        self.is_yield_last_token_to_overlapping_compound_requirement_fulfilled = self._is_yield_last_token_to_overlapping_compound_requirement_fulfilled()

        self.are_fulfilled = (self.is_yield_last_token_to_overlapping_compound_requirement_fulfilled)

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if(not self.is_yield_last_token_to_overlapping_compound_requirement_fulfilled, "yield_last_token_to_overlapping_compound")
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())

    def _is_yield_last_token_to_overlapping_compound_requirement_fulfilled(self) -> bool:
        if not self.rules.yield_last_token_to_overlapping_compound.is_set(): return True

        last_token_display_words: list[CandidateWord] = self.match().candidate().candidate_word().end_location().create_display_words_starting_here()
        if not last_token_display_words: return True

        return not last_token_display_words[0].is_custom_compound
