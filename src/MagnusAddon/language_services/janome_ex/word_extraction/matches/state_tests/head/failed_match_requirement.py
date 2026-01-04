from __future__ import annotations

from typing import override

from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement


class FailedMatchRequirement(MatchRequirement):
    def __init__(self, reason: str) -> None:
        self.reason: str = reason

    @property
    @override
    def is_fulfilled(self) -> bool: return False

    @property
    @override
    def failure_reason(self) -> str: return self.reason
