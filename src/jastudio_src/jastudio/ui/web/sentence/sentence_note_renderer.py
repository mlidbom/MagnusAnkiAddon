from __future__ import annotations

from aqt import gui_hooks
from JAStudio.Core.Note import SentenceNote
from JAStudio.Core.UI.Web.Sentence import SentenceNoteRenderer

from jastudio.sysutils import app_thread_pool
from jastudio.ui.web.web_utils.pre_rendering_content_renderer_anki_shim import PrerenderingContentRendererAnkiShim


def init() -> None:
    renderer = SentenceNoteRenderer.CreateRenderer(app_thread_pool.pool.submit)
    gui_hooks.card_will_show.append(PrerenderingContentRendererAnkiShim(SentenceNote, renderer).render)
