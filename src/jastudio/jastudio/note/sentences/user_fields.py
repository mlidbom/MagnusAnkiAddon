from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.note.note_constants import SentenceNoteFields
from jastudio.note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from jastudio.note.sentences.sentencenote import SentenceNote
    from jastudio.sysutils.weak_ref import WeakRef

class SentenceUserFields(Slots):
    def __init__(self, sentence: WeakRef[SentenceNote]) -> None:
        self._sentence: WeakRef[SentenceNote] = sentence

    @property
    def comments(self) -> MutableStringField: return MutableStringField(self._sentence, SentenceNoteFields.user_comments)
    @property
    def answer(self) -> MutableStringField: return MutableStringField(self._sentence, SentenceNoteFields.user_answer)
    @property
    def question(self) -> MutableStringField: return MutableStringField(self._sentence, SentenceNoteFields.user_question)
