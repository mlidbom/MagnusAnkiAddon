from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsShadowed(MatchRequirement, Slots):
    def __init__(self, inspector: MatchInspector) -> None:
        self.inspector: MatchInspector = inspector

    @property
    @override
    def is_fulfilled(self) -> bool:
        return not self.inspector.match.is_shadowed

    @property
    @override
    def failure_reason(self) -> str:
        return f"""forbids::shadowed_by:{self.inspector.match.word.shadowed_by_text}""" if not self.is_fulfilled else ""