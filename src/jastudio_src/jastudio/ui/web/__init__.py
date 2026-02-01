from __future__ import annotations

from jastudio.ui.web import kanji, sentence, vocab


def init() -> None:
    kanji.init()
    vocab.init()
    sentence.init()