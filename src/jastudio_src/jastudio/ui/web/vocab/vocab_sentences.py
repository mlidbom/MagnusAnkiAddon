from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaslib.ui.web.vocab import vocab_sentences_renderer

from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote,
                                                                      {"##IN_SENTENCES##": vocab_sentences_renderer.generate_valid_in_list_html,
                                                                       "##MARKED_INVALID_IN_SENTENCES##": vocab_sentences_renderer.generate_marked_invalid_in_list_html}
                                                                      ).render)
