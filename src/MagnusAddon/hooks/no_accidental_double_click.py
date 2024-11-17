from typing import Literal

from aqt.reviewer import Reviewer
from aqt.utils import tooltip
import time

from ankiutils import app
from sysutils.typed import non_optional

# noinspection PyProtectedMember
_real_show_answer = Reviewer._showAnswer
# noinspection PyProtectedMember
_real_answer_card = Reviewer._answerCard

_last_click = time.time()

def _show_answer(self:Reviewer) -> None:
    if app.config().prevent_double_clicks.get_value():
        global _last_click
        if non_optional(self.card).time_taken() < app.config().minimum_time_viewing_question.get_value() * 1000:
            tooltip("Blocked accidental doubleclick")
            return
        _last_click = time.time()
    _real_show_answer(self)

def _answer_card(self:Reviewer, ease: Literal[1, 2, 3, 4]) -> None:
    if app.config().prevent_double_clicks.get_value():
        global _last_click
        waitalil = time.time() - _last_click
        if waitalil < app.config().minimum_time_viewing_question.get_value():
            tooltip("Blocked accidental doubleclick")
            return

    _real_answer_card(self, ease)


Reviewer._showAnswer = _show_answer  # type: ignore
Reviewer._answerCard = _answer_card  # type: ignore