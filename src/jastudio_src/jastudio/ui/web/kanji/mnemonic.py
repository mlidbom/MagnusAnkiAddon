from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.kanjinote import KanjiNote
from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def render_mnemonic(note: KanjiNote) -> str:
    return note.get_active_mnemonic()

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(KanjiNote, {"##MNEMONIC##": render_mnemonic}).render)