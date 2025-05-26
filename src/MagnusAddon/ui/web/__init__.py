from __future__ import annotations

from ui.web import kanji, sentence, vocab, vocab_and_sentence_kanji_list


def init() -> None:
    kanji.init()
    vocab.init()
    sentence.init()
    vocab_and_sentence_kanji_list.init()