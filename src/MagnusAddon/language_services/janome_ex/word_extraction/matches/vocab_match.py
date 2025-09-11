from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.match import Match
from language_services.janome_ex.word_extraction.matches.requirements.display_requirements import DisplayRequirements
from language_services.janome_ex.word_extraction.matches.requirements.head_requirements import HeadRequirements
from language_services.janome_ex.word_extraction.matches.requirements.misc_requirements import MiscRequirements
from language_services.janome_ex.word_extraction.matches.requirements.tail_requirements import TailRequirements
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration

class VocabMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        super().__init__(word_variant)
        self.vocab: VocabNote = vocab
        self.word_variant: WeakRef[CandidateWordVariant] = word_variant
        self.weakref = WeakRef(self)

        self.head_requirements: HeadRequirements = HeadRequirements(self, word_variant, self.word_variant().word.start_location.previous)
        self.tail_requirements: TailRequirements = TailRequirements(self.vocab, self.word_variant().word.end_location.next)
        self.misc_requirements: MiscRequirements = MiscRequirements(self.weakref)

        self.owns_form: bool = vocab.forms.is_owned_form(self.tokenized_form)

    @property
    def matching(self) -> VocabNoteMatchingConfiguration: return self.vocab.matching_configuration
    @property
    def match_form(self) -> str: return self.vocab.get_question()
    @property
    def answer(self) -> str: return self.vocab.get_answer()
    @property
    def readings(self) -> list[str]: return self.vocab.readings.get()

    @property
    def parsed_form(self) -> str:
        if self.matching.bool_flags.question_overrides_form.is_set():
            return self.vocab.question.raw
        return super().parsed_form

    @property
    def start_index(self) -> int:
        if self.matching.bool_flags.question_overrides_form.is_set() and self.matching.configurable_rules.required_prefix.any():
            matched_prefixes = [prefix for prefix in self.matching.configurable_rules.required_prefix.get() if self.parsed_form.startswith(prefix)]
            if matched_prefixes:
                return super().start_index - max(len(prefix) for prefix in matched_prefixes)

        return super().start_index

    @property
    def _is_valid_internal(self) -> bool:
        return (super()._is_valid_internal
                and self.head_requirements.are_fulfilled
                and self.tail_requirements.are_fulfilled
                and self.misc_requirements.are_fulfilled)

    @property
    def is_secondary_match(self) -> bool: return not self.owns_form and any(other_match for other_match in self.word_variant().vocab_matches if other_match.owns_form and other_match.is_valid)

    @property
    def is_valid_for_display(self) -> bool: return super().is_valid_for_display and self.display_requirements.are_fulfilled
    @property
    def display_requirements(self) -> DisplayRequirements: return DisplayRequirements(self.weakref)

    @property
    def failure_reasons(self) -> set[str]:
        return (super().failure_reasons
                | self.misc_requirements.failure_reasons()
                | self.head_requirements.failure_reasons()
                | self.tail_requirements.failure_reasons())

    @property
    def hiding_reasons(self) -> set[str]: return (super().hiding_reasons
                                                  | self.display_requirements.failure_reasons())

    def __repr__(self) -> str: return f"""{self.vocab.get_question()}, {self.vocab.get_answer()[:10]}: {" ".join(self.failure_reasons)} {" ".join(self.hiding_reasons)}"""
