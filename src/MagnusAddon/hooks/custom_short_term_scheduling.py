from anki.scheduler.v3 import QueuedCards, SchedulingStates
from aqt.reviewer import V3CardInfo
from note.jpcard import JPCard

_seconds_to_schedule = 60

class JPSchedulingStates:
    def __init__(self, states:SchedulingStates) -> None:
        self.states = states

    def is_relearning(self) -> bool: return self.states.again.normal.relearning.learning.scheduled_secs > 0
    def is_learning(self) -> bool: return self.states.again.normal.learning.scheduled_secs > 0

    def set_again_seconds(self, seconds:int) -> None:
        if self.is_relearning():
            self.states.again.normal.relearning.learning.scheduled_secs = seconds
        elif self.is_learning():
            self.states.again.normal.learning.scheduled_secs = seconds
        else:
            raise Exception("May only be called on relearning or learning cards")

_oldMethod = V3CardInfo.from_queue
def set_again_time_for_previously_failed_today_cards(queue:QueuedCards) -> V3CardInfo:
    info = _oldMethod(queue)

    from ankiutils import app
    if app.config().decrease_failed_card_intervals.get_value():
        card = JPCard(info.top_card().card)

        if card.last_answer_today_was_fail_db_call():
            JPSchedulingStates(info.states).set_again_seconds(app.config().decrease_failed_card_intervals_interval.get_value())

    return info

V3CardInfo.from_queue = set_again_time_for_previously_failed_today_cards  # type: ignore #noqa