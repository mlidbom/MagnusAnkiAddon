from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

class NotInState(MatchRequirement, Slots):
    def __init__(self, state_test: MatchStateTest, is_requirement_active: bool = True) -> None:
        super().__init__(state_test)
        self.is_requirement_active: bool = is_requirement_active

    @property
    @override
    def is_fulfilled(self) -> bool: return (not self.is_requirement_active
                                            or not self.state_test.match_is_in_state)

    @property
    @override
    def failure_reason(self) -> str: return self.state_test.state_description if not self.is_fulfilled else ""
