from __future__ import annotations

from typing import Literal

from jastudio.ankiutils import app
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional

# noinspection PyProtectedMember
_real_show_answer = Reviewer._showAnswer  # pyright: ignore[reportPrivateUsage]
# noinspection PyProtectedMember
_real_answer_card = Reviewer._answerCard  # pyright: ignore[reportPrivateUsage]

_stopwatch = StopWatch()

def _show_answer(reviewer: Reviewer) -> None:
    if app.config().prevent_double_clicks.get_value() and mw.reviewer.auto_advance_enabled:
        global _stopwatch
        if non_optional(reviewer.card).time_taken() < app.config().minimum_time_viewing_question.get_value() * 1000:
            tooltip("Blocked accidental doubleclick")
            return
        _stopwatch = StopWatch()
    _real_show_answer(reviewer)

def _answer_card(reviewer: Reviewer, ease: Literal[1, 2, 3, 4]) -> None:
    if app.config().prevent_double_clicks.get_value() and mw.reviewer.auto_advance_enabled:
        global _stopwatch
        if _stopwatch.elapsed_seconds() < app.config().minimum_time_viewing_answer.get_value():
            tooltip("Blocked accidental doubleclick")
            return

    _real_answer_card(reviewer, ease)


def init() -> None:
    Reviewer._showAnswer = _show_answer # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
    Reviewer._answerCard = _answer_card # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
