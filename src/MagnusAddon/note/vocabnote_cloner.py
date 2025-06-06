from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from anki.notes import Note
from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules, app  # noqa
from autoslot import Slots
from language_services import conjugator
from note.note_constants import NoteTypes, Tags

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabCloner(Slots):
    def __init__(self, note: WeakRef[VocabNote]) -> None:
        self._note_ref = note

    @property
    def note(self) -> VocabNote: return self._note_ref()

    def create_prefix_version(self, prefix: str, speech_type: str = "expression", set_compounds: bool = True, truncate_characters: int = 0) -> VocabNote:
        return self._create_postfix_prefix_version(prefix, speech_type, is_prefix=True, set_compounds=set_compounds, truncate_characters=truncate_characters)

    def create_suffix_version(self, suffix: str, speech_type: str = "expression", set_compounds: bool = True, truncate_characters: int = 0) -> VocabNote:
        return self._create_postfix_prefix_version(suffix, speech_type, set_compounds=set_compounds, truncate_characters=truncate_characters)

    def _create_postfix_prefix_version(self, addendum: str, speech_type: str, is_prefix: bool = False, set_compounds: bool = True, truncate_characters: int = 0) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote

        def append_prepend_addendum(base: str) -> str:
            if not is_prefix:
                return base + addendum if truncate_characters == 0 else base[0:-truncate_characters] + addendum
            return addendum + base if truncate_characters == 0 else base[truncate_characters:] + addendum

        vocab_note = self.note
        new_vocab = VocabNote.factory.create(question=append_prepend_addendum(self.note.get_question()),
                                             answer=self.note.get_answer(),
                                             readings=[append_prepend_addendum(reading) for reading in vocab_note.readings.get()])

        if set_compounds:
            if not is_prefix:
                compounds = [self.note.get_question(), addendum]
                new_vocab.compound_parts.set(compounds)
            else:
                compounds1 = [addendum, self.note.get_question()]
                new_vocab.compound_parts.set(compounds1)

        new_vocab.parts_of_speech.set_raw_string_value(speech_type)
        new_vocab.forms.set_list([append_prepend_addendum(form) for form in self.note.forms.all_set()])
        return new_vocab

    def create_na_adjective(self) -> VocabNote:
        return self._create_postfix_prefix_version("な", "na-adjective")

    def create_no_adjective(self) -> VocabNote:
        return self._create_postfix_prefix_version("の", "expression, no-adjective")

    def create_ni_adverb(self) -> VocabNote:
        return self._create_postfix_prefix_version("に", "adverb")

    def create_to_adverb(self) -> VocabNote:
        return self._create_postfix_prefix_version("と", "to-adverb")

    def create_te_prefixed_word(self) -> VocabNote:
        return self._create_postfix_prefix_version("て", "auxiliary", is_prefix=True)

    def create_o_prefixed_word(self) -> VocabNote:
        note = self.note
        return self._create_postfix_prefix_version("お", note.parts_of_speech.raw_string_value(), is_prefix=True)

    def create_n_suffixed_word(self) -> VocabNote:
        return self._create_postfix_prefix_version("ん", "expression")

    def create_ka_suffixed_word(self) -> VocabNote:
        return self._create_postfix_prefix_version("か", "expression")

    def create_suru_verb(self, shimasu: bool = False) -> VocabNote:
        suru_verb = self._create_postfix_prefix_version("する" if not shimasu else "します", "suru verb")

        forms = list(suru_verb.forms.all_set()) + [form.replace("する", "をする") for form in suru_verb.forms.all_set()]
        suru_verb.forms.set_list(forms)

        note = self.note
        if note.parts_of_speech.is_transitive():
            value = suru_verb.parts_of_speech.raw_string_value() + ", transitive"
            suru_verb.parts_of_speech.set_raw_string_value(value)
        vocab_note = self.note
        if vocab_note.parts_of_speech.is_intransitive():
            value1 = suru_verb.parts_of_speech.raw_string_value() + ", intransitive"
            suru_verb.parts_of_speech.set_raw_string_value(value1)

        return suru_verb

    def create_shimasu_verb(self) -> VocabNote: return self.create_suru_verb(shimasu=True)

    def clone(self) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote

        clone_backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))

        for i in range(len(self.note.backend_note.fields)):
            clone_backend_note.fields[i] = self.note.backend_note.fields[i]

        clone = VocabNote(clone_backend_note)

        for related in clone.related_notes.synonyms.strings():
            clone.related_notes.synonyms.add(related)

        app.anki_collection().addNote(clone_backend_note)

        return clone

    def clone_to_form(self, form: str) -> VocabNote:
        clone = self.clone()
        clone.question.set(form)

        for tag in [tag for tag in self.note.get_tags() if tag in Tags.system_tags]:
            clone.set_tag(tag)

        return clone

    def create_ku_form(self) -> VocabNote:
        return self._create_postfix_prefix_version("く", "adverb", set_compounds=False, truncate_characters=1)

    def clone_to_derived_form(self, form_suffix: str, create_form_root: Callable[[VocabNote, str], str]) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote

        def create_full_form(form: str) -> str: return create_form_root(self.note, form) + form_suffix

        clone = VocabNote.factory.create(question=create_full_form(self.note.get_question()), answer=self.note.get_answer(), readings=[])
        clone.forms.set_list([create_full_form(form) for form in self.note.forms.all_list()])
        vocab_note = self.note
        readings = [create_full_form(reading) for reading in vocab_note.readings.get()]
        clone.readings.set(readings)
        clone.parts_of_speech.set_raw_string_value("expression")
        compounds = [self.note.get_question(), form_suffix]
        clone.compound_parts.set(compounds)
        return clone

    def _create_preview_form(self, form_suffix: str, create_form_root: Callable[[VocabNote, str], str]) -> str:
        return create_form_root(self.note, self.note.get_question()) + form_suffix

    def suffix_to_a_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_a_stem_vocab)

    def suffix_to_a_stem_preview(self, form_suffix: str) -> str:
        return self._create_preview_form(form_suffix, conjugator.get_a_stem_vocab)

    def suffix_to_i_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_i_stem_vocab)

    def suffix_to_i_stem_preview(self, form_suffix: str) -> str:
        return self._create_preview_form(form_suffix, conjugator.get_i_stem_vocab)

    def suffix_to_e_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_e_stem_vocab)

    def suffix_to_e_stem_preview(self, form_suffix: str) -> str:
        return self._create_preview_form(form_suffix, conjugator.get_e_stem_vocab)

    def suffix_to_te_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_te_stem_vocab)

    def suffix_to_te_stem_preview(self, form_suffix: str) -> str:
        return self._create_preview_form(form_suffix, conjugator.get_te_stem_vocab)

    def create_masu_form(self) -> VocabNote:
        return self.suffix_to_i_stem("ます")

    def create_te_form(self) -> VocabNote:
        return self.suffix_to_te_stem("て")

    def create_ta_form(self) -> VocabNote:
        return self.suffix_to_te_stem("た")

    def create_ba_form(self) -> VocabNote:
        return self.suffix_to_e_stem("ば")

    def create_receptive_form(self) -> VocabNote:
        result = self.suffix_to_a_stem("れる")
        compound_parts = result.compound_parts.all()
        compound_parts[-1] = "あれる"
        result.compound_parts.set(compound_parts)
        return result

    def create_causative_form(self) -> VocabNote:
        result = self.suffix_to_a_stem("せる")
        compound_parts = result.compound_parts.all()
        compound_parts[-1] = "あせる"
        result.compound_parts.set(compound_parts)
        return result

    def create_nai_form(self) -> VocabNote:
        return self.suffix_to_a_stem("ない")
