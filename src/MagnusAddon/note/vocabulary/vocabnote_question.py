from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from language_services import conjugator
from note.note_constants import Mine, NoteFields
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.lazy import Lazy
    from sysutils.weak_ref import WeakRef

class VocabStems(ProfilableAutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab

    def masu_stem(self) -> str | None:
        masu_stem = conjugator.get_i_stem_vocab(self._vocab())
        return masu_stem if masu_stem != self._vocab().question.raw else None

class VocabNoteQuestion(ProfilableAutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        field = MutableStringField(vocab, NoteFields.Vocab.question)
        self._field: MutableStringField = field
        self._raw: Lazy[str] = field.lazy_reader(lambda: field.value)
        self._without_noise_characters: Lazy[str] = field.lazy_reader(lambda: field.value.replace(Mine.VocabPrefixSuffixMarker, ""))

    @property
    def raw(self) -> str: return self._raw()
    @property
    def without_noise_characters(self) -> str: return self._without_noise_characters()

    def stems(self) -> VocabStems: return VocabStems(self._vocab)

    def set(self, value: str) -> None:
        self._field.set(value)
        if value not in self._vocab().forms.all_set():
            self._vocab().forms.set_set(self._vocab().forms.all_set() | {value})

    @override
    def __repr__(self) -> str: return self.raw
