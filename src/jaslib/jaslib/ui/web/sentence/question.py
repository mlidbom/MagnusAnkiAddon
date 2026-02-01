from __future__ import annotations

from jaslib import app
from jaslib.note.notefields.sentence_question_field import SentenceQuestionField
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def render_wbr(question: str) -> str:
    return question.replace(SentenceQuestionField.word_break_tag, "<span class='wbr_tag'>&lt;wbr&gt;</span>") \
        if app.config().show_sentence_breakdown_in_edit_mode.get_value() \
        else question

# noinspection PyUnusedFunction
def render_user_question(note: SentenceNote) -> str:
    return render_wbr(note.user.question.value)

# noinspection PyUnusedFunction
def render_source_question(note: SentenceNote) -> str:
    return render_wbr(note.source_question.value)

def init() -> None:
    # noinspection PyStatementEffect
    PrerenderingAnswerContentRenderer(SentenceNote, {  # noqa: B018
        "##USER_QUESTION##": render_user_question,
        "##SOURCE_QUESTION##": render_source_question
    }).render
