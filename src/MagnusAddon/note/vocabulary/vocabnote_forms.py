from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from ankiutils.app import col
from autoslot import Slots
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteForms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._field: CommaSeparatedStringsListField = CommaSeparatedStringsListField(vocab, NoteFields.Vocab.Forms)
        field_with_no_reference_loop = self._field
        self._value: Lazy[set[str]] = Lazy(lambda: set(field_with_no_reference_loop.get()))

    def all_raw(self) -> list[str]:
        return self._field.get()

    def all_raw_string(self) -> str:
        return self._field.raw_string_value()

    def owned_forms(self) -> set[str]:
        vocab_note = self._vocab()

        def is_owned_by_other_form_note(form: str) -> bool:
            return any(owner for owner in app.col().vocab.with_question(form) if owner != vocab_note and vocab_note.get_question() in owner.forms.all_set())

        return {form for form in vocab_note.forms.all_set() if not is_owned_by_other_form_note(form)}

    def all_set(self) -> set[str]:
        return self._value()

    def without_noise_characters(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self.all_raw()]

    def without_noise_characters_set(self) -> set[str]:
        return set(self.without_noise_characters())

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def set_set(self, forms: set[str]) -> None:
        self.set_list(list(forms))

    def set_list(self, forms: list[str]) -> None:
        self._value = Lazy.from_value(set(forms))
        self._field.set(forms)

    def remove(self, remove: str) -> None:
        self._value().discard(remove)
        self._field.remove(remove)

        for remove_note in [voc for voc in col().vocab.with_question(remove) if self._vocab().get_question() in voc.forms.all_set()]:
            remove_note.forms.remove(self._vocab().get_question())

    def add(self, add: str) -> None:
        self._value().add(add)
        self._field.add(add)

        for add_note in [voc for voc in col().vocab.with_question(add) if self._vocab().get_question() not in voc.forms.all_set()]:
            add_note.forms.add(self._vocab().get_question())
