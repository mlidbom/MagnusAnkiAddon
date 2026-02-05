from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.ui.web.sentence import sentence_note_renderer

from jastudio.sysutils import app_thread_pool
from jastudio.ui.web.web_utils.pre_rendering_content_renderer_anki_shim import PrerenderingContentRendererAnkiShim


def init() -> None:
    renderer = sentence_note_renderer.create_renderer(app_thread_pool.pool.submit)
    gui_hooks.card_will_show.append(PrerenderingContentRendererAnkiShim(SentenceNote, renderer).render)
