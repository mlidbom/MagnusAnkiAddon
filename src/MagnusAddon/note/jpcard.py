from __future__ import annotations
from anki.cards import Card
from anki import consts
from typing import TYPE_CHECKING

from sysutils.typed import str_

if TYPE_CHECKING:
    from ankiutils import app
    from anki.scheduler.v3 import Scheduler

from anki.cards import Card
from aqt.reviewer import AnswerAction
from ankiutils import app
from sysutils import ex_iterable, timeutil, typed
from sysutils.typed import str_

def _latest_day_cutoff_timestamp() -> int:
    from aqt import mw
    return mw.col.sched.day_cutoff - timeutil.SECONDS_PER_DAY

def _last_answer_today_was_fail(card: Card) -> bool:
    answers = _get_answers_since_last_day_cutoff_for_card(card)
    sequential_again_answers = len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))
    if sequential_again_answers > 0:
        return True
    else:
        return False

def _get_answers_since_last_day_cutoff_for_card(card: Card) -> list[int]:
    reviews = app.anki_db().all("SELECT ease FROM revlog WHERE cid = ? AND id > ? ORDER BY id DESC", card.id, _latest_day_cutoff_timestamp() * timeutil.MILLISECONDS_PER_SECOND)
    answers = [typed.int_(review[0]) for review in reviews]
    return answers

class JPCard:
    def __init__(self, card:Card):
        self.card = card

    @staticmethod
    def _scheduler() -> Scheduler:
        from ankiutils import app
        return app.anki_scheduler()

    def is_suspended(self) -> bool:
        return self.card.queue == consts.QUEUE_TYPE_SUSPENDED

    def suspend(self) -> None:
        if not self.is_suspended():
            self._scheduler().suspend_cards([self.card.id])

    def un_suspend(self) -> None:
        if self.is_suspended():
            self._scheduler().unsuspend_cards([self.card.id])

    def type(self) -> str:
        return str_(self.card.template()['name'])

    def last_answer_today_was_fail_db_call(self) -> bool:
        return _last_answer_today_was_fail(self.card)

    def answers_since_last_day_cutoff_db_call(self) -> list[int]:
        return _get_answers_since_last_day_cutoff_for_card(self.card)