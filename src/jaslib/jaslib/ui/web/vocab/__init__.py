from __future__ import annotations

from jaslib.ui.web.vocab import vocab_kanji_list


def init() -> None:
    from . import compound_parts, related_vocabs, vocab_sentences
    vocab_sentences.init()
    related_vocabs.init()
    compound_parts.init()
    vocab_kanji_list.init()
