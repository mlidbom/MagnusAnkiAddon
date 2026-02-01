from __future__ import annotations

from ui.web.sentence import question


def init() -> None:
    from . import ud_sentence_breakdown
    ud_sentence_breakdown.init()
    question.init()