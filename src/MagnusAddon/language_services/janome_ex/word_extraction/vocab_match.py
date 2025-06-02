from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.match import Match
from language_services.janome_ex.word_extraction.stem_requirements import StemRequirements
from language_services.janome_ex.word_extraction.tail_requirements import TailRequirements

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabMatch(Match):
    def __init__(self, candidate: WeakRef[CandidateWordVariant], vocab: VocabNote) -> None:
        super().__init__(candidate, vocab.matching_rules)
        self.vocab: VocabNote = vocab
        self.vocab_form = vocab.get_question()
        self.answer = vocab.get_answer()
        self.readings = vocab.readings.get()

        if vocab.matching_rules.question_overrides_form.is_set():
            self.parsed_form = self.vocab.get_question()

        self.stem_requirements = StemRequirements(vocab, self.candidate().candidate_word().start_location().previous)
        self.tail_requirements = TailRequirements(vocab, self.candidate().candidate_word().end_location().next)
        self.is_poison_word = vocab.matching_rules.is_poison_word.is_set()

        self.is_valid = (self.stem_requirements.are_fulfilled
                         and self.tail_requirements.are_fulfilled
                         and not self.is_poison_word)
