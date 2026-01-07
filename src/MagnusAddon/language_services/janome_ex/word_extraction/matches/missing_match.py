from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.match import Match

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement
    from sysutils.weak_ref import WeakRef

class MissingMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant]) -> None:
        super().__init__(word_variant)

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
    @property
    @override
    def failure_reasons(self) -> list[str]:
        return super().failure_reasons + ["no_dictionary_or_vocabulary_match_found"]

    @override
    def _create_display_requirements(self) -> tuple[MatchRequirement | None, ...]: return ()
    @override
    def _create_primary_validity_failures(self) -> list[FailedMatchRequirement | None]: return []
    @override
    def _create_interdependent_validity_failures(self) -> tuple[FailedMatchRequirement | None, ...]: return ()
