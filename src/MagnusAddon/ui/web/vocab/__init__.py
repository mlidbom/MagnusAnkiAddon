from __future__ import annotations


def init() -> None:
    from . import highlighted_sentences, related_vocabs
    highlighted_sentences.init()
    related_vocabs.init()
