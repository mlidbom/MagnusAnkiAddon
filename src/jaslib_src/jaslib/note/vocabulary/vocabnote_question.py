from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots

from jaslib.language_services import conjugator
from jaslib.note.note_constants import Mine, NoteFields

if TYPE_CHECKING:
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from jaslib.sysutils.weak_ref import WeakRef

class VocabStems(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab

    def masu_stem(self) -> str | None:
        masu_stem = conjugator.get_i_stem_vocab(self._vocab())
        return masu_stem if masu_stem != self._vocab().question.raw else None

class VocabNoteQuestion(Slots):
    DISAMBIGUATION_MARKER: str = ":"
    INVALID_QUESTION_MESSAGE: str = "INVALID QUESTION FORMAT. If you need to specify disambiguation, use question:disambiguation if not do NOT use : characters. More than one is invalid"
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.raw: str = ""
        self.disambiguation_name: str = ""
        self._init_value_raw()

    def _init_value_raw(self) -> None:
        value = self._vocab().get_field(NoteFields.Vocab.question)
        if VocabNoteQuestion.DISAMBIGUATION_MARKER in value:
            self.disambiguation_name = value
            parts = self.disambiguation_name.split(VocabNoteQuestion.DISAMBIGUATION_MARKER)
            if len(parts) != 2:
                self.raw = VocabNoteQuestion.INVALID_QUESTION_MESSAGE
            else:
                self.raw = parts[0]
        else:
            self.raw = value
            self.disambiguation_name = value
        if self.raw == "": self.raw = "[EMPTY]"

    @property
    def is_valid(self) -> bool: return self.raw != VocabNoteQuestion.INVALID_QUESTION_MESSAGE

    @property
    def is_disambiguated(self) -> bool: return VocabNoteQuestion.DISAMBIGUATION_MARKER in self.disambiguation_name

    @property
    def without_noise_characters(self) -> str: return self.raw.replace(Mine.VocabPrefixSuffixMarker, "")

    def stems(self) -> VocabStems: return VocabStems(self._vocab)

    def set(self, value: str) -> None:
        self._vocab().set_field(NoteFields.Vocab.question, value)
        self._init_value_raw()
        if self.raw not in self._vocab().forms.all_set():
            self._vocab().forms.set_set(self._vocab().forms.all_set() | {self.raw})

    @override
    def __repr__(self) -> str: return self.raw
