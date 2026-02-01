from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from anki.scheduler.v3 import SchedulingState, SchedulingStates  # pyright: ignore[reportMissingTypeStubs]

class SchedulingStatesEx(Slots):
    def __init__(self, states: SchedulingStates) -> None:
        self._states: SchedulingStates = states
        self.again: SchedulingStateEx = SchedulingStateEx(states.again)

class SchedulingStateEx(Slots):
    def __init__(self, state: SchedulingState) -> None:
        self._state: SchedulingState = state

    def is_relearning(self) -> bool: return self._state.normal.relearning.learning.scheduled_secs > 0
    def is_learning(self) -> bool: return self._state.normal.learning.scheduled_secs > 0
    def is_filtered_learning(self) -> bool: return self._state.filtered.rescheduling.original_state.learning.scheduled_secs > 0
    def is_filtered_relearning(self) -> bool: return self._state.filtered.rescheduling.original_state.relearning.learning.scheduled_secs > 0

    def set_seconds(self, seconds: int) -> None:
        if self.is_relearning():
            self._state.normal.relearning.learning.scheduled_secs = seconds
        elif self.is_learning():
            self._state.normal.learning.scheduled_secs = seconds
        elif self.is_filtered_relearning():
            self._state.filtered.rescheduling.original_state.relearning.learning.scheduled_secs = seconds
        elif self.is_filtered_learning():
            self._state.filtered.rescheduling.original_state.learning.scheduled_secs = seconds
        else:
            raise Exception("May only be called on relearning or learning cards")
