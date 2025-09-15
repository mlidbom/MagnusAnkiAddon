from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import SentenceNoteFields
from note.notefields.strip_html_on_read_string_field import MutableStripHtmlOnReadStringField

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from sysutils.weak_ref import WeakRef

class SentenceUserFields(Slots):
    def __init__(self, sentence: WeakRef[SentenceNote]) -> None:
        self._sentence: WeakRef[SentenceNote] = sentence
        self.comments: MutableStripHtmlOnReadStringField = MutableStripHtmlOnReadStringField(sentence, SentenceNoteFields.user_comments)
        self.question: MutableStripHtmlOnReadStringField = MutableStripHtmlOnReadStringField(sentence, SentenceNoteFields.user_question)
        self.answer: MutableStripHtmlOnReadStringField = MutableStripHtmlOnReadStringField(sentence, SentenceNoteFields.user_answer)
        self.answer_analysis: MutableStripHtmlOnReadStringField = MutableStripHtmlOnReadStringField(sentence, SentenceNoteFields.user_answer_analysis)
