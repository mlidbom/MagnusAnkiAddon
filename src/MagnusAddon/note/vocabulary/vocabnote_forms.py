from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from ankiutils.app import col
from autoslot import Slots
from note.note_constants import Mine, NoteFields
from note.notefields.comma_separated_strings_list_field_de_duplicated import CommaSeparatedStringsListFieldDeDuplicated
from sysutils import ex_sequence, ex_str
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from anki.notes import NoteId
    from note.vocabulary.vocabnote import VocabNote

class Conjugations(Slots):
    def __init__(self, forms_other: VocabNoteForms, _vocab_note: VocabNote) -> None:
        forms = [_vocab_note.get_question()] + forms_other.without_noise_characters()
        forms = ex_sequence.remove_duplicates_while_retaining_order(forms)
        primary_form = _vocab_note.question.without_noise_characters
        self.primary_form_forms: set[str] = set(_vocab_note.conjugator.get_text_matching_forms_for_primary_form())
        secondary_forms: set[str] = {form for form in forms if form != primary_form}
        self.secondary_forms_forms: set[str] = {form for form in _vocab_note.conjugator.get_text_matching_forms_for_all_form()
                                                if form not in self.primary_form_forms}

        self.secondary_forms_containing_primary_form_forms: set[str] = {sec_form for sec_form in self.secondary_forms_forms
                                                                        if any(pri_form for pri_form in self.primary_form_forms if pri_form in sec_form)}

        derived_compounds = _vocab_note.related_notes.in_compounds()
        self.derived_compound_ids: set[NoteId] = {der.get_id() for der in derived_compounds}
        self.derived_compounds_forms: set[str] = set(ex_sequence.flatten([der.conjugator.get_text_matching_forms_for_all_form() for der in derived_compounds]))

        secondary_forms_vocab_notes = ex_sequence.flatten([app.col().vocab.with_question(v) for v in secondary_forms])
        secondary_forms_with_their_own_vocab_forms = ex_sequence.flatten([f.conjugator.get_text_matching_forms_for_all_form() for f in secondary_forms_vocab_notes])

        self.secondary_forms_with_their_own_vocab_forms: list[str] = ex_str.sort_by_length_descending(secondary_forms_with_their_own_vocab_forms)
        # Create a list of compounds derived from secondary forms
        secondary_forms_derived_compounds = ex_sequence.flatten([app.col().vocab.with_compound_part(v) for v in secondary_forms])
        self.secondary_forms_derived_compounds_forms: set[str] = set(ex_sequence.flatten([der.conjugator.get_text_matching_forms_for_all_form() for der in secondary_forms_derived_compounds]))

class VocabNoteForms(WeakRefable, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        field = CommaSeparatedStringsListFieldDeDuplicated(vocab, NoteFields.Vocab.Forms)
        self._field: CommaSeparatedStringsListFieldDeDuplicated = field
        weakrefself = WeakRef(self)
        self._all_raw_set: Lazy[set[str]] = Lazy(lambda: set(weakrefself()._field.get()))
        self._conjugations: Lazy[Conjugations] = field.lazy_reader(lambda: Conjugations(self, vocab()))

        self._all_list: Lazy[list[str]] = field.lazy_reader(lambda: [ex_str.strip_brackets(form) for form in weakrefself()._field.get()])
        self._all_set: Lazy[set[str]] = field.lazy_reader(lambda: set(weakrefself()._all_list()))
        self._owned_forms: Lazy[set[str]] = field.lazy_reader(lambda: {weakrefself()._vocab().get_question()} | {ex_str.strip_brackets(form) for form in weakrefself()._all_raw_set() if form.startswith("[")})
        self._not_owned_by_other_vocab: Lazy[set[str]] = field.lazy_reader(lambda: weakrefself().___not_owned_by_other_vocab())

    @property
    def conjugations(self) -> Conjugations: return self._conjugations()

    def is_owned_form(self, form: str) -> bool: return form in self._owned_forms()

    def all_list(self) -> list[str]: return self._all_list()
    def all_set(self) -> set[str]: return self._all_set()
    def all_raw_string(self) -> str: return self._field.raw_string_value()

    def all_list_notes(self) -> list[VocabNote]:
        return ex_sequence.flatten([app.col().vocab.with_question(form) for form in self.all_list()])

    def all_list_notes_by_sentence_count(self) -> list[VocabNote]:
        def prefer_more_sentences(vocab: VocabNote) -> int:
            return -vocab.sentences.counts().total

        return sorted(self.all_list_notes(), key=prefer_more_sentences)

    def not_owned_by_other_vocab(self) -> set[str]: return self._not_owned_by_other_vocab()

    def ___not_owned_by_other_vocab(self) -> set[str]:
        vocab_note = self._vocab()

        def is_owned_by_other_form_note(form: str) -> bool:
            return any(owner for owner in app.col().vocab.with_question(form)
                       if owner != vocab_note and vocab_note.get_question() in owner.forms.all_set())

        return {form for form in vocab_note.forms.all_set() if not is_owned_by_other_form_note(form)}

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
