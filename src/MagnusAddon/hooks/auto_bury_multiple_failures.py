from typing import Literal

from anki.cards import Card
from aqt import gui_hooks, mw
from aqt.reviewer import AnswerAction, Reviewer

from ankiutils import app
from sysutils import ex_iterable, timeutil, typed

MAX_SEQUENTIAL_AGAIN_ANSWERS = 3

def latest_day_cutoff_timestamp() -> int:
    return mw.col.sched.day_cutoff - timeutil.SECONDS_PER_DAY

def get_answers_since_last_day_cutoff_for_card(card: Card) -> list[int]:
    reviews = app.anki_db().all("SELECT ease FROM revlog WHERE cid = ? AND id > ? ORDER BY id DESC", card.id, latest_day_cutoff_timestamp() * timeutil.MILLISECONDS_PER_SECOND)
    answers = [typed.int_(review[0]) for review in reviews]

    return answers

def card_answered(_reviewer: Reviewer, card: Card, answer: Literal[1, 2, 3, 4]) -> None:
    if AnswerAction(answer) == AnswerAction.ANSWER_AGAIN:
        answers = get_answers_since_last_day_cutoff_for_card(card)
        sequential_again_answers = len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))
        if sequential_again_answers >= MAX_SEQUENTIAL_AGAIN_ANSWERS:
            print(f"card {card.id} has {sequential_again_answers} sequential again answers today. Burying it.")
            app.anki_scheduler().bury_cards([card.id])


def init() -> None:
    gui_hooks.reviewer_did_answer_card.append(card_answered)