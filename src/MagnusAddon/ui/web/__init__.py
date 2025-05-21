from __future__ import annotations

from ui.web import kanji, ud_sentence_breakdown, vocab, vocab_and_sentence_kanji_list


def init() -> None:
    kanji.init()
    vocab.init()
    ud_sentence_breakdown.init()
    vocab_and_sentence_kanji_list.init()