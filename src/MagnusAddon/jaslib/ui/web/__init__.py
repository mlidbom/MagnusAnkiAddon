from __future__ import annotations

from jaslib.ui.web import kanji, sentence, vocab


# noinspection PyUnusedFunction
def init() -> None:
    kanji.init()
    vocab.init()
    sentence.init()