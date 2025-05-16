from __future__ import annotations

import re
from typing import TYPE_CHECKING

from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from sysutils.ex_sequence import ExSequence

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteForms:
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._field: CommaSeparatedStringsListField = CommaSeparatedStringsListField(vocab, NoteFields.Vocab.Forms)

    def all_raw(self) -> list[str]: return self._field.get()

    def all_raw_string(self) -> str:
        return self._field.raw_string_value()

    def unexcluded_list(self) -> list[str]: return ExSequence.filter(self._field.get(), self._is_excluded_form, invert_condition=True)
    def unexcluded_set(self) -> set[str]: return set(self.unexcluded_list())

    def unexcluded_without_noise_characters(self) -> list[str]: return [self._strip_noise_characters(form) for form in self.unexcluded_list()]
    def unexcluded_without_noise_characters_set(self) -> set[str]: return set(self.unexcluded_without_noise_characters())

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    _forms_exclusions = re.compile(r"\[\[|]]")
    def _is_excluded_form(self, form: str) -> bool:
        return self._forms_exclusions.search(form) is not None

    def excluded_set(self) -> set[str]:
        def strip_brackets(form: str) -> str: return self._forms_exclusions.sub("", form)

        return set(ExSequence.transform(ExSequence.filter(self.all_raw(), self._is_excluded_form),
                                        strip_brackets))

    def set_set(self, forms: set[str]) -> None: self.set_list(list(forms))
    def set_list(self, forms: list[str]) -> None: self._field.set(forms)
