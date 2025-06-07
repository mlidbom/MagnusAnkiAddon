from __future__ import annotations

from ankiutils import app
from aqt import gui_hooks
from note.notefields.sentence_question_field import SentenceQuestionField
from note.sentences.sentencenote import SentenceNote
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def render_user_question(note: SentenceNote) -> str:
    return note.user.question.get_raw() \
        if not app.config().show_sentence_breakdown_in_edit_mode.get_value() \
        else note.user.question.get_raw().replace(SentenceQuestionField.word_break_tag, "&lt;wbr&gt;")

def render_source_question(note: SentenceNote) -> str:
    return note.source_question.get_raw() \
        if not app.config().show_sentence_breakdown_in_edit_mode.get_value() \
        else note.source_question.get_raw().replace(SentenceQuestionField.word_break_tag, "&lt;wbr&gt;")

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
        "##USER_QUESTION##": render_user_question,
        "##SOURCE_QUESTION##": render_source_question
    }).render)
