from __future__ import annotations


def init() -> None:
    from . import context_sentences, highlighted_sentences, related_vocabs  # noqa: F401
    context_sentences.init()
    highlighted_sentences.init()
    related_vocabs.init()
