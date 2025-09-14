from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields
from note.notefields.string_field import AutoStrippingStringField
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class VocabNoteUserfields(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.mnemonic: AutoStrippingStringField = AutoStrippingStringField(vocab, NoteFields.Vocab.user_mnemonic)
        self.answer: AutoStrippingStringField = AutoStrippingStringField(vocab, NoteFields.Vocab.user_answer)
        self.explanation: AutoStrippingStringField = AutoStrippingStringField(vocab, NoteFields.Vocab.user_explanation)
        self.explanation_long: AutoStrippingStringField = AutoStrippingStringField(vocab, NoteFields.Vocab.user_explanation_long)
