from __future__ import annotations

from ui.web import kanji, sentence, vocab
from ui.web.vocab import vocab_kanji_list


def init() -> None:
    kanji.init()
    vocab.init()
    sentence.init()