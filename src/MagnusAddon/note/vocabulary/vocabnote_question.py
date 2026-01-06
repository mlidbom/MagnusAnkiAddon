from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services import conjugator
from note.note_constants import Mine, NoteFields

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabStems(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab

    def masu_stem(self) -> str | None:
        masu_stem = conjugator.get_i_stem_vocab(self._vocab())
        return masu_stem if masu_stem != self._vocab().question.raw else None

class VocabNoteQuestion(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.raw: str = ""
        self.disambiguation_name: str = ""
        self.is_valid = True
        self._init_value_raw()

    def _init_value_raw(self) -> None:
        value = self._vocab().get_field(NoteFields.Vocab.question)
        if value.startswith("["):
            self.disambiguation_name = value[1:-1]
            parts = self.disambiguation_name.split(":")
            if len(parts) != 2:
                self.is_valid = False
                self.raw = "INVALID QUESTION FORMAT. If you need to specify disambiguation, use [question:disambiguation] if not do NOT use [] characters"
            else:
                self.raw = parts[0]
        else:
            self.raw = value
            self.disambiguation_name = value
        if self.raw == "": self.raw = "[EMPTY]"

    @property
    def is_disambiguated(self) -> bool: return ":" in self.disambiguation_name

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
