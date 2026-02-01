from __future__ import annotations

from jaslib.note.kanjinote import KanjiNote
from jaslib.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def render_mnemonic(note: KanjiNote) -> str:
    return note.get_active_mnemonic()

def init() -> None:
    # noinspection PyStatementEffect
    PrerenderingAnswerContentRenderer(KanjiNote, {"##MNEMONIC##": render_mnemonic}).render  # noqa: B018
