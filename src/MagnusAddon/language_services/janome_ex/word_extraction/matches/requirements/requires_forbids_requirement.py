from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirementWithStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
    from note.notefields.require_forbid_flag_field import RequireForbidFlagField


class RequiresOrForbids(MatchRequirementWithStateTest, Slots):
    def __init__(self, state_test: MatchStateTest, requires_forbids: RequireForbidFlagField) -> None:
        super().__init__(state_test)
        self.is_required: bool = requires_forbids.is_required
        self.is_forbidden: bool = requires_forbids.is_forbidden

    @property
    @override
    def is_fulfilled(self) -> bool:
        if self.is_required and not self.state_test.match_is_in_state:
            return False

        if self.is_forbidden and self.state_test.match_is_in_state:  # noqa: SIM103 these returns are useful for breakpoints when debugging
            return False

        return True

    @property
    @override
    def failure_reason(self) -> str:
        if self.is_fulfilled:
            return ""

        if self.is_required:
            return f"required::{self.state_test.description}"

        if self.is_forbidden:
            return f"forbids::{self.state_test.description}"

        raise AssertionError("This should never happen")
