from __future__ import annotations

from typing import TYPE_CHECKING

from anki import consts
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.anki_extentions.deck_ex import DeckEx
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from anki.dbproxy import Row
    from anki.decks import DeckManager
    from anki.scheduler.v3 import Scheduler  # pyright: ignore[reportMissingTypeStubs]
    from jastudio.anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
    from jastudio.note.jpnote import JPNote

import anki.cards
import anki.cards_pb2
from aqt.reviewer import AnswerAction
from jastudio.ankiutils import app
from sysutils import timeutil, typed


def _latest_day_cutoff_timestamp() -> int:
    from aqt import mw
    return non_optional(mw.col).sched.day_cutoff - timeutil.SECONDS_PER_DAY

def _get_answers_since_last_day_cutoff_for_card(card_id: int) -> QList[int]:
    with StopWatch.log_warning_if_slower_than(0.01):
        reviews: list[Row] = app.anki_db().all("SELECT ease FROM revlog WHERE cid = ? AND id > ? ORDER BY id DESC", card_id, _latest_day_cutoff_timestamp() * timeutil.MILLISECONDS_PER_SECOND)
        return QList(typed.int_(review[0]) for review in reviews)  # pyright: ignore[reportAny]

class CardEx(Slots):
    def __init__(self, card:anki.cards.Card) -> None:
        self.card:anki.cards.Card = card

    @classmethod
    def _scheduler(cls) -> Scheduler:
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
        from jastudio.anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
        return NoteTemplateEx.from_dict(self.card.template())

    def sequential_again_answers_today(self) -> int:
        answers = _get_answers_since_last_day_cutoff_for_card(self.card.id)
        return answers.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN).qcount() # len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))

    def note(self) -> JPNote:
        from jastudio.note.jpnote import JPNote
        return JPNote.note_from_card(self.card)

    @classmethod
    def _deck_manager(cls) -> DeckManager:
        return app.anki_collection().decks

    def get_deck(self) -> DeckEx:
        return DeckEx(non_optional(self._deck_manager().get(self.card.current_deck_id())))


class Card2Ex(Slots):
    def __init__(self, card:anki.cards_pb2.Card) -> None:
        self.card:anki.cards_pb2.Card = card

    def sequential_again_answers_today(self) -> int:
        answers = _get_answers_since_last_day_cutoff_for_card(self.card.id)
        return answers.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN).qcount()  #len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))

    def last_answer_today_was_fail_db_call(self) -> bool:
        return self.sequential_again_answers_today() > 0