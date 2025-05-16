from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.strip_html_on_read_string_field import StripHtmlOnReadStringField
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote

class SentenceUserFields:
    def __init__(self, sentence: SentenceNote) -> None:
        self._sentence = sentence
        self.comments: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_comments)
        self.comments_long: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_comments_long)
        self.question: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_question)
        self.answer: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_answer)
        self.answer_analysis: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_answer_analysis)
        self._instance_tracker = ObjectInstanceTracker(SentenceUserFields)
