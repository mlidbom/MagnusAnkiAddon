from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.note_constants import SentenceNoteFields
from note.notefields.caching_mutable_string_field import CachingMutableStringField
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from sysutils.weak_ref import WeakRef

class SentenceUserFields(Slots):
    def __init__(self, sentence: WeakRef[SentenceNote]) -> None:
        self._sentence: WeakRef[SentenceNote] = sentence
        self.comments: MutableStringField = MutableStringField(sentence, SentenceNoteFields.user_comments)
        self.question: CachingMutableStringField = CachingMutableStringField(sentence, SentenceNoteFields.user_question)
        self.answer: MutableStringField = MutableStringField(sentence, SentenceNoteFields.user_answer)
        self.answer_analysis: MutableStringField = MutableStringField(sentence, SentenceNoteFields.user_answer_analysis)
