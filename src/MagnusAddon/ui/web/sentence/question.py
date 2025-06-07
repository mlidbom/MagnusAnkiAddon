from __future__ import annotations

from ankiutils import app
from aqt import gui_hooks
from note.notefields.sentence_question_field import SentenceQuestionField
from note.sentences.sentencenote import SentenceNote
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def render_wbr(question: str) -> str:
    return question.replace(SentenceQuestionField.word_break_tag, "<span class='wbr_tag'>&lt;wbr&gt;</span>") \
        if app.config().show_sentence_breakdown_in_edit_mode.get_value() \
        else question

def render_user_question(note: SentenceNote) -> str:
    return render_wbr(note.user.question.get_raw())

def render_source_question(note: SentenceNote) -> str:
    return render_wbr(note.source_question.get_raw())

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(SentenceNote, {
        "##USER_QUESTION##": render_user_question,
        "##SOURCE_QUESTION##": render_source_question
    }).render)
