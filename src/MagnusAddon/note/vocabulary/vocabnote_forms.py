from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from ankiutils.app import col
from ex_autoslot import ProfilableAutoSlots
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field_de_duplicated import MutableCommaSeparatedStringsListFieldDeDuplicated
from sysutils import ex_sequence, ex_str
from sysutils.collections.linq.q_iterable import QSet
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteForms(WeakRefable, ProfilableAutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        field = MutableCommaSeparatedStringsListFieldDeDuplicated(vocab, NoteFields.Vocab.Forms)
        self._field: MutableCommaSeparatedStringsListFieldDeDuplicated = field
        weakrefthis = WeakRef(self)
        self._all_raw_set: Lazy[set[str]] = Lazy(lambda: set(weakrefthis()._field.get()))

        self._all_list: Lazy[list[str]] = field.lazy_reader(lambda: [ex_str.strip_brackets(form) for form in weakrefthis()._field.get()])
        self._all_set: Lazy[QSet[str]] = field.lazy_reader(lambda: QSet(weakrefthis()._all_list()))
        self._owned_forms: Lazy[set[str]] = field.lazy_reader(lambda: {weakrefthis()._vocab().get_question()} | {ex_str.strip_brackets(form) for form in weakrefthis()._all_raw_set() if form.startswith("[")})
        self._not_owned_by_other_vocab: Lazy[QSet[str]] = field.lazy_reader(lambda: weakrefthis().___not_owned_by_other_vocab())

    def is_owned_form(self, form: str) -> bool: return form in self._owned_forms()

    def all_list(self) -> list[str]: return self._all_list()
    def all_set(self) -> QSet[str]: return self._all_set()
    def all_raw_string(self) -> str: return self._field.raw_string_value()

    def all_list_notes(self) -> list[VocabNote]:
        return ex_sequence.flatten([app.col().vocab.with_question(form) for form in self.all_list()])

    def all_list_notes_by_sentence_count(self) -> list[VocabNote]:
        def prefer_more_sentences(vocab: VocabNote) -> int:
            return -vocab.sentences.counts().total

        return sorted(self.all_list_notes(), key=prefer_more_sentences)

    def not_owned_by_other_vocab(self) -> QSet[str]: return self._not_owned_by_other_vocab()

    def ___not_owned_by_other_vocab(self) -> QSet[str]:
        vocab_note = self._vocab()

        def is_not_owned_by_other_form_note(form: str) -> bool:
            return (app.col().vocab.with_question(form)
                    .where(lambda form_owning_vocab:
                           form_owning_vocab != vocab_note
                           and vocab_note.get_question() in form_owning_vocab.forms.all_set())
                    .none())
            # return not any(owner for owner in app.col().vocab.with_question(form)
            #                if owner != vocab_note and vocab_note.get_question() in owner.forms.all_set())

        return vocab_note.forms.all_set().where(is_not_owned_by_other_form_note).to_set()  # {form for form in vocab_note.forms.all_set() if not is_owned_by_other_form_note(form)}

    def without_noise_characters(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self.all_list()]

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def set_set(self, forms: set[str]) -> None: self.set_list(list(forms))

    def set_list(self, forms: list[str]) -> None: self._field.set(forms)

    def remove(self, remove: str) -> None:
        self._field.remove(remove)

        for remove_note in [voc for voc in col().vocab.with_question(remove) if self._vocab().get_question() in voc.forms.all_set()]:
            remove_note.forms.remove(self._vocab().get_question())

    def add(self, add: str) -> None:
        self._field.add(add)

        for add_note in [voc for voc in col().vocab.with_question(add) if self._vocab().get_question() not in voc.forms.all_set()]:
            add_note.forms.add(self._vocab().get_question())

    @override
    def __repr__(self) -> str: return self._field.__repr__()
