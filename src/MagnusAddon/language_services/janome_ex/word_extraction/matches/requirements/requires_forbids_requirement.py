from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
    from note.notefields.require_forbid_flag_field import RequireForbidFlagField


class RequiresForbidsRequirement(MatchRequirement, Slots):
    def __init__(self, state_test: MatchStateTest, requires_forbids: RequireForbidFlagField) -> None:
        super().__init__(state_test)
        self.requires_forbids: RequireForbidFlagField = requires_forbids

    @property
    def is_required(self) -> bool: return self.requires_forbids.is_required
    @property
    def is_forbidden(self) -> bool: return self.requires_forbids.is_forbidden

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
            return f"required::{self.state_test.name}"

        if self.is_forbidden:
            return f"forbids::{self.state_test.name}"

        raise AssertionError("This should never happen")
