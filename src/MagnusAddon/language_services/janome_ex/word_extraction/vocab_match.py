from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.match import Match
from language_services.janome_ex.word_extraction.stem_requirements import StemRequirements

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabMatch(Match):
    def __init__(self, candidate: WeakRef[CandidateWord], vocab: VocabNote) -> None:
        super().__init__(candidate)
        self.vocab: VocabNote = vocab
        self.vocab_form = vocab.get_question()
        self.answer = vocab.get_answer()
        self.readings = vocab.readings.get()

        if vocab.matching_rules.question_overrides_form.is_set():
            self.parsed_form = self.vocab.get_question()

        self.stem_requirements = StemRequirements(vocab, self.candidate().prefix)

        self.is_valid = self.stem_requirements.are_fulfilled
