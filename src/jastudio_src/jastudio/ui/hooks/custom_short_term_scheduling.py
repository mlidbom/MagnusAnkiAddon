from __future__ import annotations

from typing import TYPE_CHECKING

from aqt.reviewer import V3CardInfo
from jaspythonutils.sysutils.timeutil import StopWatch

from jastudio.anki_extentions.card_ex import Card2Ex
from jastudio.anki_extentions.sheduling_states_ex import SchedulingStatesEx
from jastudio.ankiutils import app

if TYPE_CHECKING:
    from anki.scheduler.v3 import QueuedCards  # pyright: ignore[reportMissingTypeStubs]

_oldMethod = V3CardInfo.from_queue
def set_again_time_for_previously_failed_today_cards(queue:QueuedCards) -> V3CardInfo:
    with StopWatch.log_warning_if_slower_than(0.01):
        info = _oldMethod(queue)

        if app.is_initialized() and app.config().DecreaseFailedCardIntervals.GetValue():
            card = Card2Ex(info.top_card().card)

            if card.last_answer_today_was_fail_db_call():
                SchedulingStatesEx(info.states).again.set_seconds(app.config().DecreaseFailedCardIntervalsInterval.GetValue())

        return info

def init() -> None:
    V3CardInfo.from_queue = set_again_time_for_previously_failed_today_cards  # type: ignore  # pyright: ignore[reportAttributeAccessIssue]