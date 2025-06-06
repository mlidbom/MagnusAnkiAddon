from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.match import Match

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from sysutils.weak_ref import WeakRef


class MissingMatch(Match):
    def __init__(self, candidate: WeakRef[CandidateWordVariant]) -> None:
        super().__init__(candidate, None)
        self.answer = "---"
        self.match_form = "[MISSING]" #Change this so the tests can distinguish that this is a missing match

    @property
    def is_primary_match(self) -> bool: return True