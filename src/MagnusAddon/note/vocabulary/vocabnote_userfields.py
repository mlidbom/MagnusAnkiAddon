from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class VocabNoteUserfields(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.mnemonic: MutableStringField = MutableStringField(vocab, NoteFields.Vocab.user_mnemonic)
        self.answer: MutableStringField = MutableStringField(vocab, NoteFields.Vocab.user_answer)
