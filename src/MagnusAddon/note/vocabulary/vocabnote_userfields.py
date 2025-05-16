from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields
from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


class VocabNoteUserfields:
    def __init__(self, vocab: VocabNote) -> None:
        self.mnemonic: StringField = StringField(vocab, NoteFields.Vocab.user_mnemonic)
        self.answer: StringField = StringField(vocab, NoteFields.Vocab.user_answer)
        self.explanation: StringField = StringField(vocab, NoteFields.Vocab.user_explanation)
        self.explanation_long: StringField = StringField(vocab, NoteFields.Vocab.user_explanation_long)
