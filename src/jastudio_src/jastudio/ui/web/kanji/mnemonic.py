from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.kanjinote import KanjiNote
from jaslib.ui.web.kanji import mnemonic_renderer

from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(KanjiNote, {"##MNEMONIC##": mnemonic_renderer.render_mnemonic}).render)