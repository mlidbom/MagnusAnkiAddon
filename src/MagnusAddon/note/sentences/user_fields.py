from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import SentenceNoteFields
from note.notefields.strip_html_on_read_string_field import StripHtmlOnReadStringField
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from sysutils.weak_ref import WeakRef

class SentenceUserFields(Slots):
    def __init__(self, sentence: WeakRef[SentenceNote]) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self._sentence: WeakRef[SentenceNote] = sentence
        self.comments: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_comments)
        self.question: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_question)
        self.answer: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_answer)
        self.answer_analysis: StripHtmlOnReadStringField = StripHtmlOnReadStringField(sentence, SentenceNoteFields.user_answer_analysis)
