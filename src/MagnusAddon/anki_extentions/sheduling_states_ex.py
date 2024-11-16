from anki.scheduler.v3 import SchedulingStates

class SchedulingStatesEx:
    def __init__(self, states:SchedulingStates) -> None:
        self.states = states

    def is_relearning(self) -> bool: return self.states.again.normal.relearning.learning.scheduled_secs > 0
    def is_learning(self) -> bool: return self.states.again.normal.learning.scheduled_secs > 0
    def is_filtered_learning(self) -> bool: return self.states.again.filtered.rescheduling.original_state.learning.scheduled_secs > 0
    def is_filtered_relearning(self) -> bool: return self.states.again.filtered.rescheduling.original_state.relearning.learning.scheduled_secs > 0

    def set_again_seconds(self, seconds:int) -> None:
        if self.is_relearning():
            self.states.again.normal.relearning.learning.scheduled_secs = seconds
        elif self.is_learning():
            self.states.again.normal.learning.scheduled_secs = seconds
        elif self.is_filtered_relearning():
            self.states.again.filtered.rescheduling.original_state.relearning.learning.scheduled_secs = seconds
        elif self.is_filtered_learning():
            self.states.again.filtered.rescheduling.original_state.learning.scheduled_secs = seconds
        else:
            raise Exception("May only be called on relearning or learning cards")
