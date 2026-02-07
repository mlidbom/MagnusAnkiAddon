from __future__ import annotations

from typing import Literal

from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from jaspythonutils.sysutils.timeutil import StopWatch
from jaspythonutils.sysutils.typed import non_optional

from jastudio.ankiutils import app

# noinspection PyProtectedMember
_real_show_answer = Reviewer._showAnswer  # pyright: ignore[reportPrivateUsage]
# noinspection PyProtectedMember
_real_answer_card = Reviewer._answerCard  # pyright: ignore[reportPrivateUsage]

_stopwatch = StopWatch()

def _show_answer(reviewer: Reviewer) -> None:
    if app.config().PreventDoubleClicks.GetValue() and mw.reviewer.auto_advance_enabled:
        global _stopwatch
        if non_optional(reviewer.card).time_taken() < app.config().MinimumTimeViewingQuestion.GetValue() * 1000:
            tooltip("Blocked accidental doubleclick")
            return
        _stopwatch = StopWatch()
    _real_show_answer(reviewer)

def _answer_card(reviewer: Reviewer, ease: Literal[1, 2, 3, 4]) -> None:
    if app.config().PreventDoubleClicks.GetValue() and mw.reviewer.auto_advance_enabled:
        global _stopwatch
        if _stopwatch.elapsed_seconds() < app.config().MinimumTimeViewingAnswer.GetValue():
            tooltip("Blocked accidental doubleclick")
            return

    _real_answer_card(reviewer, ease)


def init() -> None:
    Reviewer._showAnswer = _show_answer # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
    Reviewer._answerCard = _answer_card # type: ignore  # pyright: ignore[reportAttributeAccessIssue, reportPrivateUsage]
