from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.ankiutils import app
from jastudio.ankiutils.app import col
from jastudio.note.note_constants import Mine, NoteFields
from jastudio.note.notefields.comma_separated_strings_list_field_de_duplicated import MutableCommaSeparatedStringsListFieldDeDuplicated
from jastudio.sysutils import ex_str
from jastudio.sysutils.lazy import Lazy
from jastudio.sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_set import QSet
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from jastudio.note.vocabulary.vocabnote import VocabNote
    from typed_linq_collections.collections.q_list import QList

# todo performance: memory: this class seems to be using a ton of memory. Do we need all of this cached?
class VocabNoteForms(WeakRefable, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        field = MutableCommaSeparatedStringsListFieldDeDuplicated(vocab, NoteFields.Vocab.Forms)
        self._field: MutableCommaSeparatedStringsListFieldDeDuplicated = field
        weakrefthis = WeakRef(self)
        self._all_raw_set: Lazy[QSet[str]] = Lazy(lambda: QSet(weakrefthis()._field.get()))

        self._all_list: Lazy[QList[str]] = field.lazy_reader(lambda: query(weakrefthis()._field.get()).select(ex_str.strip_brackets).to_list()) # [ex_str.strip_brackets(form) for form in weakrefthis()._field.get()]
        self._all_set: Lazy[QSet[str]] = field.lazy_reader(lambda: weakrefthis()._all_list().to_set())
        self._owned_forms: Lazy[QSet[str]] = field.lazy_reader(lambda: QSet([weakrefthis()._vocab().get_question()]) | QSet(ex_str.strip_brackets(form) for form in weakrefthis()._all_raw_set() if form.startswith("[")))
        self._not_owned_by_other_vocab: Lazy[QSet[str]] = field.lazy_reader(lambda: weakrefthis().___not_owned_by_other_vocab())

    def is_owned_form(self, form: str) -> bool: return form in self._owned_forms()

    def all_list(self) -> QList[str]: return self._all_list()
    def all_set(self) -> QSet[str]: return self._all_set()
    def all_raw_string(self) -> str: return self._field.raw_string_value()

    def all_list_notes(self) -> QList[VocabNote]:
        return self._all_list().select_many(app.col().vocab.with_question).to_list() #ex_sequence.flatten([app.col().vocab.with_question(form) for form in self.all_list()])


    def all_list_notes_by_sentence_count(self) -> list[VocabNote]:
        def prefer_more_sentences(vocab: VocabNote) -> int:
            return -vocab.sentences.counts().total

        return sorted(self.all_list_notes(), key=prefer_more_sentences)

    def not_owned_by_other_vocab(self) -> QSet[str]: return self._not_owned_by_other_vocab()

    def ___not_owned_by_other_vocab(self) -> QSet[str]:
        vocab_note = self._vocab()

        def is_not_owned_by_other_form_note(form: str) -> bool:
            return (query(app.col().vocab.with_question(form))
                    .where(lambda form_owning_vocab:
                           form_owning_vocab != vocab_note
                           and vocab_note.get_question() in form_owning_vocab.forms.all_set())
                    .none())
            # return not any(owner for owner in app.col().vocab.with_question(form)
            #                if owner != vocab_note and vocab_note.get_question() in owner.forms.all_set())

        return vocab_note.forms.all_set().where(is_not_owned_by_other_form_note).to_set()  # {form for form in vocab_note.forms.all_set() if not is_owned_by_other_form_note(form)}

    def without_noise_characters(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self.all_list()]

    @classmethod
    def _strip_noise_characters(cls, string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def set_set(self, forms: QSet[str]) -> None: self.set_list(list(forms))

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
