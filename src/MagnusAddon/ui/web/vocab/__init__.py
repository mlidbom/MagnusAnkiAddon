from __future__ import annotations

from ui.web.vocab import vocab_kanji_list


def init() -> None:
    from . import compound_parts, highlighted_sentences, related_vocabs
    highlighted_sentences.init()
    related_vocabs.init()
    compound_parts.init()
    vocab_kanji_list.init()
