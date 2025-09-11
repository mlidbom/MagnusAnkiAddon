from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.matches.match import Match

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from sysutils.weak_ref import WeakRef

class MissingMatch(Match):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant]) -> None:
        super().__init__(word_variant, None)
        self.answer = "---"
        self.match_form = "[MISSING]"  # Change this so the tests can distinguish that this is a missing match

    @property
    def is_secondary_match(self) -> bool: return True

    @property
    def is_valid(self) -> bool: return False
