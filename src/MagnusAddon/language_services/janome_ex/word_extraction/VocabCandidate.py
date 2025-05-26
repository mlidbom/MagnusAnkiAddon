from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabCandidate:
    def __init__(self, candidate: WeakRef[CandidateWord], vocab: VocabNote) -> None:
        self.vocab: VocabNote = vocab
        self.candidate: WeakRef[CandidateWord] = candidate

        self.rules = vocab.matching_rules
        rules = self.rules

        self.is_exact_match = candidate().form == vocab.question.without_noise_characters()

        self.is_valid_match = (not rules.requires_exact_match.is_set() or self.is_exact_match)

    def __repr__(self) -> str: return (
        SkipFalsyValuesDebugReprBuilder()
        .include(self.vocab.question.raw())
        .flag("is_valid_match", self.is_valid_match)
        .flag("is_exact_match", self.is_exact_match)
        .repr)
