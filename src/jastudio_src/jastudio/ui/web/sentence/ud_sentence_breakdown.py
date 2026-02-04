from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.ui.web.sentence import ud_sentence_breakdown_renderer

from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
            "##SENTENCE_ANALYSIS##": ud_sentence_breakdown_renderer.render_sentence_analysis
    }).render)
