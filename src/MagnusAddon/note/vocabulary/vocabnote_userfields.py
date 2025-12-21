from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.note_constants import NoteFields
from note.notefields.caching_mutable_string_field import CachingMutableStringField
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteUserfields(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.answer: CachingMutableStringField = CachingMutableStringField(vocab, NoteFields.Vocab.user_answer)
        self.mnemonic: MutableStringField = MutableStringField(vocab, NoteFields.Vocab.user_mnemonic)
        self.explanation: MutableStringField = MutableStringField(vocab, NoteFields.Vocab.user_explanation)
        self.explanation_long: MutableStringField = MutableStringField(vocab, NoteFields.Vocab.user_explanation_long)

    @override
    def __repr__(self) -> str: return f"Answer: {self.answer.value}, Mnemonic: {self.mnemonic.value}, Explanation: {self.explanation.value}, Explanation Long: {self.explanation_long.value}"
