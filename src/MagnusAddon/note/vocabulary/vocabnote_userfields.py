from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields
from note.notefields.string_field import StringField
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class VocabNoteUserfields:
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.mnemonic: StringField = StringField(vocab, NoteFields.Vocab.user_mnemonic)
        self.answer: StringField = StringField(vocab, NoteFields.Vocab.user_answer)
        self.explanation: StringField = StringField(vocab, NoteFields.Vocab.user_explanation)
        self.explanation_long: StringField = StringField(vocab, NoteFields.Vocab.user_explanation_long)
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker(self.__class__)
