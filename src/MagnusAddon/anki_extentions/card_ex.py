from __future__ import annotations

from typing import TYPE_CHECKING

from anki import consts
from anki_extentions.deck_ex import DeckEx
from ex_autoslot import ProfilableAutoSlots
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from anki.dbproxy import Row
    from anki.decks import DeckManager
    from anki.scheduler.v3 import Scheduler  # pyright: ignore[reportMissingTypeStubs]
    from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
    from note.jpnote import JPNote

import anki.cards
import anki.cards_pb2
from ankiutils import app
from aqt.reviewer import AnswerAction
from sysutils import ex_iterable, timeutil, typed


def _latest_day_cutoff_timestamp() -> int:
    from aqt import mw
    return non_optional(mw.col).sched.day_cutoff - timeutil.SECONDS_PER_DAY

def _get_answers_since_last_day_cutoff_for_card(card_id: int) -> list[int]:
    with StopWatch.log_warning_if_slower_than(0.01):
        reviews: list[Row] = app.anki_db().all("SELECT ease FROM revlog WHERE cid = ? AND id > ? ORDER BY id DESC", card_id, _latest_day_cutoff_timestamp() * timeutil.MILLISECONDS_PER_SECOND)
        return [typed.int_(review[0]) for review in reviews]  # pyright: ignore[reportAny]

class CardEx(ProfilableAutoSlots):
    def __init__(self, card:anki.cards.Card) -> None:
        self.card:anki.cards.Card = card

    @staticmethod
    def _scheduler() -> Scheduler:
        return app.anki_scheduler()

    def is_suspended(self) -> bool:
        return self.card.queue == consts.QUEUE_TYPE_SUSPENDED

    def suspend(self) -> None:
        if not self.is_suspended():
            self._scheduler().suspend_cards([self.card.id])

    def un_suspend(self) -> None:
        if self.is_suspended():
            self._scheduler().unsuspend_cards([self.card.id])

    def type(self) -> NoteTemplateEx:
        from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
        return NoteTemplateEx.from_dict(self.card.template())

    def sequential_again_answers_today(self) -> int:
        answers = _get_answers_since_last_day_cutoff_for_card(self.card.id)
        return len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))

    def note(self) -> JPNote:
        from note.jpnote import JPNote
        return JPNote.note_from_card(self.card)

    @staticmethod
    def _deck_manager() -> DeckManager:
        return app.anki_collection().decks

    def get_deck(self) -> DeckEx:
        return DeckEx(non_optional(self._deck_manager().get(self.card.current_deck_id())))


class Card2Ex(ProfilableAutoSlots):
    def __init__(self, card:anki.cards_pb2.Card) -> None:
        self.card:anki.cards_pb2.Card = card

    def sequential_again_answers_today(self) -> int:
        answers = _get_answers_since_last_day_cutoff_for_card(self.card.id)
        return len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))

    def last_answer_today_was_fail_db_call(self) -> bool:
        return self.sequential_again_answers_today() > 0