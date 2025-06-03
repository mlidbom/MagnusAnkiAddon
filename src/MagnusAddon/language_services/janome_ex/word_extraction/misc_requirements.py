from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.simple_string_list_builder import SimpleStringListBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class MiscRequirements(Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        vocab = match().vocab
        rules = vocab.matching_rules

        self.is_poison_word = rules.is_poison_word.is_set()
        self.is_exact_match_requirement_fulfilled = (not rules.requires_exact_match.is_set()
                                                     or match().candidate().form == vocab.question.without_noise_characters())

        self.are_fulfilled = (self.is_exact_match_requirement_fulfilled
                              and (not self.is_poison_word
                                   or not match().candidate().candidate_word().is_custom_compound  # todo: bug: This absolutely does not belong here. Figure out how to get rid of it without tests failing.
                                   ))

    def failure_reasons(self) -> set[str]:
        return (SimpleStringListBuilder()
                .append_if("fails_exact_match_requirement", not self.is_exact_match_requirement_fulfilled)
                .append_if("is_poison_word", self.is_poison_word)
                .as_set())

    def __repr__(self) -> str: return " ".join(self.failure_reasons())
