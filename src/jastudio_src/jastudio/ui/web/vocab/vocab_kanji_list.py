from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaslib.ui.web.vocab import vocab_kanji_list_renderer

from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##KANJI_LIST##": vocab_kanji_list_renderer.render_vocab_kanji_list}).render)
