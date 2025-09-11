from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from note.note_constants import Mine, NoteFields
from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.lazy import Lazy
    from sysutils.weak_ref import WeakRef

class VocabStems(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab = vocab

    def masu_stem(self) -> str | None:
        masu_stem = conjugator.get_i_stem_vocab(self._vocab())
        return masu_stem if masu_stem != self._vocab().question.raw else None

class VocabNoteQuestion(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab = vocab
        field = StringField(vocab, NoteFields.Vocab.question)
        self._field = field
        self._raw: Lazy[str] = field.lazy_reader(lambda: field.get())
        self._without_noise_characters: Lazy[str] = field.lazy_reader(lambda: field.get().replace(Mine.VocabPrefixSuffixMarker, ""))

    @property
    def raw(self) -> str: return self._raw()
    @property
    def without_noise_characters(self) -> str: return self._without_noise_characters()

    def stems(self) -> VocabStems: return VocabStems(self._vocab)

    def set(self, value: str) -> None: self._field.set(value)
