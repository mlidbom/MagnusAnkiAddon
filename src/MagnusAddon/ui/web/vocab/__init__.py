from __future__ import annotations


def init() -> None:
    from . import compound_parts, highlighted_sentences, related_vocabs
    highlighted_sentences.init()
    related_vocabs.init()
    compound_parts.init()
