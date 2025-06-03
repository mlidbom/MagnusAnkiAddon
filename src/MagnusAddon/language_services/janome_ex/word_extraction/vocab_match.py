from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
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

        if vocab.matching_rules.question_overrides_form.is_set():
            self.parsed_form = self.vocab.get_question()

        self.stem_requirements = StemRequirements(vocab, self.candidate().candidate_word().start_location().previous)
        self.tail_requirements = TailRequirements(vocab, self.candidate().candidate_word().end_location().next)
        self.misc_requirements = MiscRequirements(self.weakref)

        self.is_valid = (self.stem_requirements.are_fulfilled
                         and self.tail_requirements.are_fulfilled
                         and self.misc_requirements.are_fulfilled)  # if we remove ourselves and we are not a compound, part of the text goes missing

    def failure_reasons(self) -> set[str]:
        return (self.misc_requirements.failure_reasons()
                | self.stem_requirements.failure_reasons()
                | self.tail_requirements.failure_reasons())
