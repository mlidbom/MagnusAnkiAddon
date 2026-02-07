from __future__ import annotations


def init() -> None:
    from jastudio.ui.web.kanji import kanji_note_renderer
    kanji_note_renderer.init()