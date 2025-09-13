from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.state_tests.match_state_test import MatchStateTest

class MatchRequirement(Slots):
    @property
    def is_fulfilled(self) -> bool: raise NotImplementedError()

class MustBeInStateMatchRequirement(MatchRequirement, Slots):
    def __init__(self, state_test: MatchStateTest) -> None:
        self.state_test: MatchStateTest = state_test

    @property
    def is_fulfilled(self) -> bool: return self.state_test.match_is_in_state
