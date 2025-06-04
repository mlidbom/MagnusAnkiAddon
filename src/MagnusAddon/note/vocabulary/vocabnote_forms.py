from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from ankiutils.app import col
from autoslot import Slots
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field_de_duplicated import CommaSeparatedStringsListFieldDeDuplicated
from sysutils import ex_sequence, ex_str
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteForms(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._field: CommaSeparatedStringsListFieldDeDuplicated = CommaSeparatedStringsListFieldDeDuplicated(vocab, NoteFields.Vocab.Forms)
        weakrefself = WeakRef(self)
        self._all_raw: Lazy[set[str]] = Lazy(lambda: set(weakrefself()._field.get()))

    def _owned_forms(self) -> set[str]: return {self._vocab().get_question()} | {ex_str.strip_brackets(form) for form in self._all_raw() if form.startswith("[")}

    def is_owned_form(self, form: str) -> bool: return form in self._owned_forms()

    def all_list(self) -> list[str]:
        return [ex_str.strip_brackets(form) for form in self._field.get()]

    def all_list_notes(self) -> list[VocabNote]:
        return ex_sequence.flatten([app.col().vocab.with_question(form) for form in self.all_list()])

    def all_list_notes_by_sentence_count(self) -> list[VocabNote]:
        def prefer_more_sentences(vocab: VocabNote) -> int:
            return -vocab.sentences.counts().total

        return sorted(self.all_list_notes(), key=prefer_more_sentences)

    def all_raw_string(self) -> str:
        return self._field.raw_string_value()

    def not_owned_by_other_vocab(self) -> set[str]:
        vocab_note = self._vocab()

        def is_owned_by_other_form_note(form: str) -> bool:
            return any(owner for owner in app.col().vocab.with_question(form) if owner != vocab_note and vocab_note.get_question() in owner.forms.all_set())

        return {form for form in vocab_note.forms.all_set() if not is_owned_by_other_form_note(form)}

    def all_set(self) -> set[str]:
        return {ex_str.strip_brackets(form) for form in self._all_raw()}

    def without_noise_characters(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self.all_list()]

    def without_noise_characters_set(self) -> set[str]:
        return set(self.without_noise_characters())

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def set_set(self, forms: set[str]) -> None:
        self.set_list(list(forms))

    def set_list(self, forms: list[str]) -> None:
        self._all_raw = Lazy.from_value(set(forms))
        self._field.set(forms)

    def remove(self, remove: str) -> None:
        self._all_raw().discard(remove)
        self._field.remove(remove)

        for remove_note in [voc for voc in col().vocab.with_question(remove) if self._vocab().get_question() in voc.forms.all_set()]:
            remove_note.forms.remove(self._vocab().get_question())

    def add(self, add: str) -> None:
        self._all_raw().add(add)
        self._field.add(add)

        for add_note in [voc for voc in col().vocab.with_question(add) if self._vocab().get_question() not in voc.forms.all_set()]:
            add_note.forms.add(self._vocab().get_question())
