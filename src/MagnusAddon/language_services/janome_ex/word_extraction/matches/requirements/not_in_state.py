from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

class NotInState(MatchRequirement, ProfilableAutoSlots):
    def __init__(self, state_test: MatchStateTest, is_requirement_active: bool = True) -> None:
        super().__init__(state_test)
        self.is_requirement_active: bool = is_requirement_active

    @property
    @override
    def is_fulfilled(self) -> bool:
        if not self.is_requirement_active:
            return True

        if not self.state_test.match_is_in_state:  # noqa: SIM103
            return True

        return False

    @property
    @override
    def failure_reason(self) -> str: return f"""forbids::{self.state_test.state_description}""" if not self.is_fulfilled else ""
