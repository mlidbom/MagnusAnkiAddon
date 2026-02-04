from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaslib.ui.web.vocab import vocab_note_renderer

from jastudio.sysutils import app_thread_pool
from jastudio.ui.web.web_utils.pre_rendering_content_renderer_anki_shim import PrerenderingContentRendererAnkiShim


def init() -> None:
    renderer = vocab_note_renderer.create_renderer(app_thread_pool.pool.submit)
    gui_hooks.card_will_show.append(PrerenderingContentRendererAnkiShim(VocabNote, renderer).render)
