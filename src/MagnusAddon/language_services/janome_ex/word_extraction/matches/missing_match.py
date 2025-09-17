from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from language_services.janome_ex.word_extraction.matches.match import Match

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from sysutils.weak_ref import WeakRef

class MissingMatch(Match, ProfilableAutoSlots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant]) -> None:
        super().__init__(word_variant, validity_requirements=[], display_requirements=[])

    @property
    @override
    def answer(self) -> str: return "---"
    @property
    @override
    def match_form(self) -> str: return "[MISSING]"  # Change this so the tests can distinguish that this is a missing match
    @property
    @override
    def is_valid(self) -> bool: return False
    @property
    @override
    def readings(self) -> list[str]: return []
