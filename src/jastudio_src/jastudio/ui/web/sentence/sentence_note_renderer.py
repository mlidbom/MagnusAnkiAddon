from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.ui.web.sentence import sentence_renderer, ud_sentence_breakdown_renderer

from jastudio.ui.web.web_utils.pre_rendering_content_renderer_anki_shim import PrerenderingContentRendererAnkiShim


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingContentRendererAnkiShim(SentenceNote, {
        "##USER_QUESTION##": sentence_renderer.render_user_question,
        "##SOURCE_QUESTION##": sentence_renderer.render_source_question,
        "##SENTENCE_ANALYSIS##": ud_sentence_breakdown_renderer.render_sentence_analysis,
    }).render)
