from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest


class MatchRequirement(Slots):
    def __init__(self, state_test: MatchStateTest) -> None:
        self.state_test: MatchStateTest = state_test

    @property
    def is_fulfilled(self) -> bool: raise NotImplementedError()

    @property
    def failure_reason(self) -> str: raise NotImplementedError()

    @override
    def __repr__(self) -> str: return self.failure_reason

class MustBeInStateMatchRequirement(MatchRequirement, Slots):
    def __init__(self, state_test: MatchStateTest) -> None:
        super().__init__(state_test)

    @property
    @override
    def is_fulfilled(self) -> bool: return self.state_test.match_is_in_state

    @property
    @override
    def failure_reason(self) -> str: return f"not_{self.state_test.state_description}"

class MustNotBeInStateMatchRequirement(MatchRequirement, Slots):
    def __init__(self, state_test: MatchStateTest) -> None:
        super().__init__(state_test)

    @property
    @override
    def is_fulfilled(self) -> bool: return not self.state_test.match_is_in_state

    @property
    @override
    def failure_reason(self) -> str: return self.state_test.state_description or ""
