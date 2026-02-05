from __future__ import annotations

from aqt import gui_hooks
from JAStudio.Core.Note import KanjiNote
from JAStudio.Core.UI.Web.Kanji import KanjiNoteRenderer

from jastudio.sysutils import app_thread_pool
from jastudio.ui.web.web_utils.pre_rendering_content_renderer_anki_shim import PrerenderingContentRendererAnkiShim


def init() -> None:
    renderer = KanjiNoteRenderer.CreateRenderer(app_thread_pool.pool.submit)
    gui_hooks.card_will_show.append(PrerenderingContentRendererAnkiShim(KanjiNote, renderer).render)
