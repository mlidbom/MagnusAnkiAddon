from typing import Literal

from anki.cards import Card
from aqt import gui_hooks
from aqt.reviewer import AnswerAction, Reviewer

from ankiutils import app
from note.jpcard import JPCard
from sysutils import ex_iterable

MAX_SEQUENTIAL_AGAIN_ANSWERS = 3


def card_answered(_reviewer: Reviewer, anki_card: Card, answer: Literal[1, 2, 3, 4]) -> None:
    if AnswerAction(answer) == AnswerAction.ANSWER_AGAIN:
        card = JPCard(anki_card)
        answers = card.answers_since_last_day_cutoff_db_call()
        sequential_again_answers = len(list(ex_iterable.take_while(lambda x: AnswerAction(x) == AnswerAction.ANSWER_AGAIN, answers)))
        if sequential_again_answers >= MAX_SEQUENTIAL_AGAIN_ANSWERS:
            print(f"card {anki_card.id} has {sequential_again_answers} sequential again answers today. Burying it.")
            app.anki_scheduler().bury_cards([anki_card.id])


def init() -> None:
    gui_hooks.reviewer_did_answer_card.append(card_answered)