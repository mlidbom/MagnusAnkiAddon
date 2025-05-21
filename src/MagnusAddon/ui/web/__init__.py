from __future__ import annotations

from ui.web import kanji, radical_and_kanji_kanji_kanji_list, ud_sentence_breakdown, vocab, vocab_and_sentence_kanji_list


def init() -> None:
    kanji.init()
    vocab.init()
    radical_and_kanji_kanji_kanji_list.init()
    ud_sentence_breakdown.init()
    vocab_and_sentence_kanji_list.init()