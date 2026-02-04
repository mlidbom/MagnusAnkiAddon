from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.note.notefields.sentence_question_field import SentenceQuestionField
from jastudio.ankiutils import app

if TYPE_CHECKING:
    from jaslib.note.sentences.sentencenote import SentenceNote


def render_wbr(question: str) -> str:
    return question.replace(SentenceQuestionField.word_break_tag, "<span class='wbr_tag'>&lt;wbr&gt;</span>") \
        if app.config().show_sentence_breakdown_in_edit_mode.get_value() \
        else question

def render_user_question(note: SentenceNote) -> str:
    return render_wbr(note.user.question.value)

def render_source_question(note: SentenceNote) -> str:
    return render_wbr(note.source_question.value)
