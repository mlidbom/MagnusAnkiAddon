from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.display_requirements import DisplayRequirements
from language_services.janome_ex.word_extraction.match import Match
from language_services.janome_ex.word_extraction.misc_requirements import MiscRequirements
from language_services.janome_ex.word_extraction.stem_requirements import StemRequirements
from language_services.janome_ex.word_extraction.tail_requirements import TailRequirements
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote

class VocabMatch(Match, Slots):
    def __init__(self, candidate: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        super().__init__(candidate, vocab.matching_rules)
        self.vocab: VocabNote = vocab
        self.weakref = WeakRef(self)
        self.vocab_form = vocab.get_question()
        self.answer = vocab.get_answer()
        self.readings = vocab.readings.get()
        self.stem_requirements: StemRequirements = StemRequirements(self.vocab, self.candidate().candidate_word().start_location().previous)
        self.tail_requirements: TailRequirements = TailRequirements(self.vocab, self.candidate().candidate_word().end_location().next)
        self.misc_requirements: MiscRequirements = MiscRequirements(self.weakref)

        if vocab.matching_rules.question_overrides_form.is_set():
            self.parsed_form = self.vocab.get_question()

    @property
    def is_valid(self) -> bool:
        return (super().is_valid
                and self.stem_requirements.are_fulfilled
                and self.tail_requirements.are_fulfilled
                and self.misc_requirements.are_fulfilled)

    @property
    def is_valid_for_display(self) -> bool: return (super().is_valid_for_display
                                                    and self.is_valid and self.display_requirements.are_fulfilled)
    @property
    def display_requirements(self) -> DisplayRequirements: return DisplayRequirements(self.weakref)

    @property
    def failure_reasons(self) -> set[str]:
        return (super().failure_reasons
                | self.misc_requirements.failure_reasons()
                | self.stem_requirements.failure_reasons()
                | self.tail_requirements.failure_reasons()
                | self.display_requirements.failure_reasons())

    def __repr__(self) -> str: return " ".join(self.failure_reasons)
