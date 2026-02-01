from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.note.note_constants import NoteFields
from jastudio.note.notefields.caching_mutable_string_field import CachingMutableStringField
from jastudio.note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from jaslib.sysutils.weak_ref import WeakRef
    from jastudio.note.vocabulary.vocabnote import VocabNote

class VocabNoteUserfields(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.answer: CachingMutableStringField = CachingMutableStringField(vocab, NoteFields.Vocab.user_answer)

    @property
    def mnemonic(self) -> MutableStringField: return MutableStringField(self._vocab, NoteFields.Vocab.user_mnemonic)
    @property
    def explanation(self) -> MutableStringField: return MutableStringField(self._vocab, NoteFields.Vocab.user_explanation)
    @property
    def explanation_long(self) -> MutableStringField: return MutableStringField(self._vocab, NoteFields.Vocab.user_explanation_long)

    @override
    def __repr__(self) -> str: return f"Answer: {self.answer.value}, Mnemonic: {self.mnemonic.value}, Explanation: {self.explanation.value}, Explanation Long: {self.explanation_long.value}"
