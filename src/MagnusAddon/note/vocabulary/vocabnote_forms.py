from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteForms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._field: CommaSeparatedStringsListField = CommaSeparatedStringsListField(vocab, NoteFields.Vocab.Forms)

    def all_raw(self) -> list[str]: return self._field.get()

    def all_raw_string(self) -> str:
        return self._field.raw_string_value()

    def all_set(self) -> set[str]: return set(self.all_raw())

    def without_noise_characters(self) -> list[str]: return [self._strip_noise_characters(form) for form in self.all_raw()]
    def without_noise_characters_set(self) -> set[str]: return set(self.without_noise_characters())

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def set_set(self, forms: set[str]) -> None: self.set_list(list(forms))
    def set_list(self, forms: list[str]) -> None: self._field.set(forms)
