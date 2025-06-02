from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWordVariant
    from sysutils.weak_ref import WeakRef


class Match(Slots):
    def __init__(self, candidate: WeakRef[CandidateWordVariant]) -> None:
        self.candidate: WeakRef[CandidateWordVariant] = candidate
        self.parsed_form: str = candidate().form
        self.vocab_form: str = ""
        self.answer: str = ""
        self.readings: list[str] = []
