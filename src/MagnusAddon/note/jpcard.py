from __future__ import annotations
from anki.cards import Card
from anki import consts
from typing import TYPE_CHECKING

from sysutils.typed import checked_cast, str_

if TYPE_CHECKING:
    from ankiutils import app
    from anki.scheduler.v3 import Scheduler

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