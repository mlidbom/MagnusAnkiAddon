from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from sysutils.object_instance_tracker import ObjectInstanceTracker  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest


class MatchRequirement(Slots):
    def __init__(self, state_test: MatchStateTest) -> None:
        self.object_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self.state_test: MatchStateTest = state_test

    @property
    def is_fulfilled(self) -> bool: raise NotImplementedError()

    @property
    def failure_reason(self) -> str: raise NotImplementedError()

    @override
    def __repr__(self) -> str: return self.failure_reason

