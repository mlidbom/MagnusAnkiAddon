from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.vocab_match_state_test import VocabMatchStateTest
    from note.notefields.require_forbid_flag_field import RequireForbidFlagField


class RequiresForbidsRequirement:
    def __init__(self, state_test: VocabMatchStateTest, requires_forbids: RequireForbidFlagField) -> None:
        self.requires_forbids: RequireForbidFlagField = requires_forbids
        self.state_test: VocabMatchStateTest = state_test

    @property
    def is_required(self) -> bool: return self.requires_forbids.is_required
    @property
    def is_forbidden(self) -> bool: return self.requires_forbids.is_forbidden

    def is_fulfilled(self) -> bool:
        if self.is_required and not self.state_test.match_is_in_state:
            return False

        if self.is_forbidden and not self.state_test.match_is_in_state:  # noqa: SIM103 these returns are useful for breakpoints when debugging
            return False

        return True

    def failure_message(self) -> str:
        if self.is_required and not self.state_test.match_is_in_state:
            return f"{self.state_test.name}_is_required"

        if self.is_forbidden and not self.state_test.match_is_in_state:  # noqa: SIM103 these returns are useful for breakpoints when debugging
            return f"{self.state_test.name}_is_forbidden"

        return ""
