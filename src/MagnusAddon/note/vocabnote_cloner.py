from __future__ import annotations
from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa

from language_services import conjugator
from note.note_constants import Mine

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from note.vocabnote import VocabNote

class VocabCloner:
    def __init__(self, note: VocabNote):
        self.note = note

    def create_prefix_version(self, prefix: str, speech_type: str = "expression", set_compounds: bool = True, truncate_characters: int = 0) -> VocabNote:
        return self._create_postfix_prefix_version(prefix, speech_type, is_prefix=True, set_compounds=set_compounds, truncate_characters=truncate_characters)

    def create_suffix_version(self, suffix: str, speech_type: str = "expression", set_compounds: bool = True, truncate_characters: int = 0) -> VocabNote:
        return self._create_postfix_prefix_version(suffix, speech_type, set_compounds=set_compounds, truncate_characters=truncate_characters)

    def _create_postfix_prefix_version(self, addendum: str, speech_type: str, is_prefix: bool = False, set_compounds: bool = True, truncate_characters: int = 0) -> VocabNote:
        def append_prepend_addendum(base: str) -> str:
            if not is_prefix:
                return base + addendum if truncate_characters == 0 else base[0:-truncate_characters] + addendum
            return addendum + base if truncate_characters == 0 else base[truncate_characters:] + addendum

        new_vocab = self.note.create(question=append_prepend_addendum(self.note.get_question()),
                                     answer=self.note.get_answer(),
                                     readings=[append_prepend_addendum(reading) for reading in self.note.get_readings()])

        if set_compounds:
            if not is_prefix:
                new_vocab.set_user_compounds([self.note.get_question(), addendum])
            else:
                new_vocab.set_user_compounds([addendum, self.note.get_question()])

        new_vocab.set_speech_type(speech_type)
        new_vocab.set_forms(set([append_prepend_addendum(form) for form in self.note.get_forms()]))
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
        return self._create_postfix_prefix_version("お", self.note.get_speech_type(), is_prefix=True)

    def create_n_suffixed_word(self) -> VocabNote:
        return self._create_postfix_prefix_version("ん", "expression")

    def create_ka_suffixed_word(self) -> VocabNote:
        return self._create_postfix_prefix_version("か", "expression")

    def create_suru_verb(self, shimasu: bool = False) -> VocabNote:
        suru_verb = self._create_postfix_prefix_version("する" if not shimasu else "します", "suru verb")

        forms = list(suru_verb.get_forms()) + [form.replace("する", "をする") for form in suru_verb.get_forms()]
        suru_verb.set_forms(set(forms))

        if self.note.is_transitive(): suru_verb.set_speech_type(suru_verb.get_speech_type() + ", transitive")
        if self.note.is_intransitive(): suru_verb.set_speech_type(suru_verb.get_speech_type() + ", intransitive")

        return suru_verb

    def create_shimasu_verb(self) -> VocabNote: return self.create_suru_verb(shimasu=True)

    def clone_to_form(self, form: str) -> VocabNote:
        clone = self.note.clone()
        clone.set_question(form)

        for tag in [tag for tag in self.note.get_tags() if tag in Mine.Tags.system_tags]:
            clone.set_tag(tag)

        return clone

    def create_ku_form(self) -> VocabNote:
        return self._create_postfix_prefix_version("く", "adverb", set_compounds=False, truncate_characters=1)

    def clone_to_derived_form(self, form_suffix: str, create_form_root: Callable[[VocabNote, str], str]) -> VocabNote:
        def create_full_form(form: str) -> str: return create_form_root(self.note, form) + form_suffix

        clone = self.note.create(question=create_full_form(self.note.get_question()), answer=self.note.get_answer(), readings=[])
        clone.set_forms(set(create_full_form(form) for form in self.note.get_forms()))
        clone.set_readings([create_full_form(reading) for reading in self.note.get_readings()])
        clone.set_speech_type("expression")
        clone.set_user_compounds([self.note.get_question(), form_suffix])
        return clone

    def suffix_to_a_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_a_stem_vocab)

    def suffix_to_i_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_i_stem_vocab)

    def suffix_to_e_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_e_stem_vocab)

    def suffix_to_te_stem(self, form_suffix: str) -> VocabNote:
        return self.clone_to_derived_form(form_suffix, conjugator.get_te_stem_vocab)

    def create_masu_form(self) -> VocabNote:
        return self.suffix_to_i_stem("ます")

    def create_te_form(self) -> VocabNote:
        return self.suffix_to_te_stem("て")

    def create_ta_form(self) -> VocabNote:
        return self.suffix_to_te_stem("た")
