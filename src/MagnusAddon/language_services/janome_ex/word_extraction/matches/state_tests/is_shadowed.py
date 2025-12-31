from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class IsShadowed(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match)

    @property
    @override
    def description(self) -> str: return "shadowed"

    @property
    @override
    def match_is_in_state(self) -> bool: return self.match.is_shadowed

    @property
    @override
    def state_description(self) -> str:
        return f"shadowed_by:{self.match.word.shadowed_by_text}" \
            if self.match_is_in_state \
            else "forbids::shadowed"
