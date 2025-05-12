from __future__ import annotations

import re
from typing import TYPE_CHECKING

import language_services.conjugator
from anki.notes import Note
from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.jamdict_ex.priority_spec import PrioritySpec
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import Mine, NoteFields, NoteTypes
from note.notefields.string_field import StringField
from note.notefields.string_set_field import StringSetField
from note.vocabnote_cloner import VocabCloner
from note.vocabulary import vocabnote_context_sentences, vocabnote_meta_tag, vocabnote_wanikani_extensions
from note.waninote import WaniNote
from sysutils import ex_sequence, ex_str, kana_utils

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.sentencenote import SentenceNote
    from wanikani_api import models

class VocabNote(WaniNote):
    def __init__(self, note: Note) -> None:
        super().__init__(note)
        self.cloner = VocabCloner(self)
        self.user_mnemonic = StringField(self, NoteFields.Vocab.Mnemonic__)
        self.similar_meanings = StringSetField(self, NoteFields.Vocab.Related_similar_meaning)

    def __repr__(self) -> str: return f"""{self.get_question()}"""

    def set_kanji(self, value: str) -> None: self.set_field(NoteFields.Vocab.Kanji, value)

    _forms_exclusions = re.compile(r'\[\[.*]]')
    def _is_excluded_form(self, form: str) -> bool:
        return bool(self._forms_exclusions.search(form))

    def get_forms(self) -> set[str]: return set(self.get_forms_list())
    def get_forms_without_noise_characters(self) -> set[str]: return set(self.get_forms_list_without_noise_characters())
    def get_forms_list(self) -> list[str]: return [form for form in ex_str.extract_comma_separated_values(self._get_forms()) if not self._is_excluded_form(form)]
    def get_forms_list_without_noise_characters(self) -> list[str]: return [self._strip_noise_characters(form) for form in self.get_forms_list()]
    def get_excluded_forms(self) -> set[str]: return set(form.replace("[[", "").replace("]]", "") for form in ex_str.extract_comma_separated_values(self._get_forms()) if self._is_excluded_form(form))
    def set_forms(self, forms: set[str]) -> None: self._set_forms(", ".join([form.strip() for form in forms]))
    def _get_forms(self) -> str: return self.get_field(NoteFields.Vocab.Forms)
    def _set_forms(self, value: str) -> None: self.set_field(NoteFields.Vocab.Forms, value)
    def get_user_compounds(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.user_compounds))
    def set_user_compounds(self, compounds: list[str]) -> None:
        self.set_field(NoteFields.Vocab.user_compounds, ",".join(compounds))

    def in_compounds(self) -> list[VocabNote]:
        from ankiutils import app
        return app.col().vocab.with_compound_part(self.get_question_without_noise_characters())

    def get_direct_dependencies(self) -> set[JPNote]:
        return (set(self.collection.kanji.with_any_kanji_in(list(self.extract_main_form_kanji()))) |
                set(ex_sequence.flatten([self.collection.vocab.with_question(compound_part) for compound_part in self.get_user_compounds()])))

    def update_generated_data(self) -> None:
        self.set_field(NoteFields.Vocab.sentence_count, str(len(self.get_sentences())))
        self.set_field(NoteFields.Vocab.active_answer, self.get_answer())

        from language_services.jamdict_ex.dict_lookup import DictLookup

        super().update_generated_data()

        question = self.get_question_without_noise_characters().strip()
        readings = ",".join(self.get_readings())

        if not readings and kana_utils.is_only_kana(question):
            self.set_readings([question])
            self.set_tag(Mine.Tags.UsuallyKanaOnly)

        if len(self.get_user_compounds()) == 0 and self._is_suru_verb_included():
            self.set_user_compounds([question[:-2], "する"])

        if self.get_question():
            lookup = DictLookup.try_lookup_vocab_word_or_name(self)
            if lookup.is_uk() and not self.has_tag(Mine.Tags.DisableKanaOnly):
                self.set_tag(Mine.Tags.UsuallyKanaOnly)

            if not self.get_forms():
                if lookup.found_words():
                    self.set_forms(lookup.valid_forms(self.is_uk()))

                if self.get_question() not in self.get_forms():
                    self.set_forms(self.get_forms() | {self.get_question()})

                if self.is_uk() and self.get_readings()[0] not in self.get_forms():
                    self.set_forms(self.get_forms() | set(self.get_readings()))

            speech_types = self.get_speech_types() - {'Unknown',
                                                      'Godan verbIchidan verb'  # crap inserted by bug in yomitan
                                                      }
            if len(speech_types) == 0:
                self.auto_set_speech_type()

    def _is_suru_verb_included(self) -> bool:
        question = self.get_question_without_noise_characters()
        return question[-2:] == "する"

    def auto_set_speech_type(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup

        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if lookup.found_words():
            self.set_speech_type(", ".join(lookup.parts_of_speech()))
        elif self._is_suru_verb_included():
            question = self.get_question_without_noise_characters()[:-2]
            readings = [reading[:-2] for reading in self.get_readings()]
            lookup = DictLookup.try_lookup_word_or_name(question, readings)
            pos = lookup.parts_of_speech() & {"transitive", "intransitive"}
            self.set_speech_type("suru verb, " + ", ".join(pos))

    def extract_main_form_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.character_is_kanji(char)]

    def extract_all_kanji(self) -> set[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question() + self._get_forms())
        return set(char for char in clean if kana_utils.character_is_kanji(char))

    def is_uk(self) -> bool: return self.has_tag(Mine.Tags.UsuallyKanaOnly)

    def set_reading_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_reading_mnemonic, value)

    def get_readings(self) -> list[str]: return ex_str.extract_comma_separated_values(self._get_reading())
    def set_readings(self, readings: list[str]) -> None: self._set_reading(", ".join([reading.strip() for reading in readings]))

    def _get_reading(self) -> str: return self.get_field(NoteFields.Vocab.Reading)
    def _set_reading(self, value: str) -> None: self.set_field(NoteFields.Vocab.Reading, value)

    def set_component_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Vocab.component_subject_ids, value)

    def priority_spec(self) -> PrioritySpec:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        return lookup.priority_spec() if lookup else PrioritySpec(set())

    def get_primary_audio(self) -> str:
        if self.get_audio_male():
            return self.get_audio_male()
        elif self.get_audio_female():
            return self.get_audio_female()
        else:
            return ""

    def get_primary_audio_path(self) -> str:
        primary_audio = self.get_primary_audio().strip()
        if not primary_audio:
            return ""

        primary_list = primary_audio.replace("[sound:", "").split("]")
        return primary_list[0]

    def get_sentences(self) -> list[SentenceNote]:
        from ankiutils import app
        return app.col().sentences.with_vocab(self)

    def get_sentences_with_owned_form(self) -> list[SentenceNote]:
        from ankiutils import app
        return app.col().sentences.with_vocab_owned_form(self)

    def get_sentences_with_primary_form(self) -> list[SentenceNote]:
        from ankiutils import app
        return app.col().sentences.with_form(self.get_question())

    def get_user_highlighted_sentences(self) -> list[SentenceNote]:
        from ankiutils import app
        return [sentence for sentence in app.col().sentences.with_highlighted_vocab(self)]

    def get_sentences_studying(self) -> list[SentenceNote]:
        return [sentence for sentence in self.get_sentences() if sentence.is_studying()]

    def get_meta_tags_html(self: VocabNote, display_extended_sentence_statistics: bool = True) -> str:
        return vocabnote_meta_tag.get_meta_tags_html(self, display_extended_sentence_statistics)

    def generate_and_set_answer(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.set_user_answer(generated)

    def can_generate_sentences_from_context_sentences(self, require_audio: bool) -> bool:
        return vocabnote_context_sentences.can_generate_sentences_from_context_sentences(self, require_audio)

    def generate_sentences_from_context_sentences(self, require_audio: bool) -> None:
        vocabnote_context_sentences.generate_sentences_from_context_sentences(self, require_audio)

    @classmethod
    def create_with_dictionary(cls, question: str) -> VocabNote:
        dict_entry = DictLookup.lookup_word_shallow(question)
        if not dict_entry.found_words(): return cls.create(question, "TODO", [])
        readings = list(set(ex_sequence.flatten([ent.kana_forms() for ent in dict_entry.entries])))
        created = cls.create(question, "TODO", readings)
        created.generate_and_set_answer()
        return created

    @classmethod
    def create(cls, question: str, answer: str, readings: list[str]) -> VocabNote:
        from ankiutils import app
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note = VocabNote(backend_note)
        note.set_question(question)
        note.set_user_answer(answer)
        note.set_readings(readings)
        note.update_generated_data()
        app.anki_collection().addNote(backend_note)
        return note

    def requires_exact_match(self) -> bool:
        return self.has_tag(Mine.Tags.requires_exact_match)

    def is_ichidan(self) -> bool:
        return "ichidan" in self.get_speech_type().lower()

    def is_godan(self) -> bool:
        return "ichidan" in self.get_speech_type().lower()

    def _get_stems_for_form(self, form: str) -> list[str]:
        return [base for base in language_services.conjugator.get_word_stems(form, is_ichidan_verb=self.is_ichidan()) if base != form]

    def get_stems_for_primary_form(self) -> list[str]:
        return ex_sequence.remove_duplicates_while_retaining_order(self._get_stems_for_form(self.get_question()))

    def get_text_matching_forms_for_primary_form(self) -> list[str]:
        return [self.get_question_without_noise_characters()] + self._get_stems_for_form(self.get_question_without_noise_characters())

    def get_text_matching_forms_for_all_form(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self.get_forms_list() + self.get_stems_for_all_forms()]

    def get_stems_for_all_forms(self) -> list[str]:
        return ex_sequence.flatten([self._get_stems_for_form(form) for form in self.get_forms()])

    def clone(self) -> VocabNote:
        clone = self.create(self.get_question(), self.get_answer(), self.get_readings())

        for i in range(len(self._note.fields)):
            clone._note.fields[i] = self._note.fields[i]

        for related in clone.get_related_similar_meaning():
            clone.add_related_similar_meaning(related)

        clone._flush()

        return clone

    def is_question_overrides_form(self) -> bool: return self.has_tag(Mine.Tags.question_overrides_form)

    def auto_generate_compounds(self) -> None:
        from ankiutils import app
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        analysis = TextAnalysis(self.get_question(), {WordExclusion(form) for form in self.get_forms()})
        compound_parts = [a.form for a in analysis.display_words if a.form not in self.get_forms()]
        if not len(compound_parts) > 1:#time to brute force it
            word = self.get_question()
            all_substrings = [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1) if word[i:j] != word]
            all_word_substrings = [w for w in all_substrings if DictLookup.is_dictionary_or_collection_word(w)]
            compound_parts = [segment for segment in all_word_substrings if not any(parent for parent in all_word_substrings if segment in parent and parent != segment)]

        segments_missing_vocab = [segment for segment in compound_parts if not app.col().vocab.is_word(segment)]
        for missing in segments_missing_vocab:
            created = VocabNote.create_with_dictionary(missing)
            created.suspend_all_cards()

        self.set_user_compounds(compound_parts)

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")

    def get_question_without_noise_characters(self) -> str: return self._strip_noise_characters(self.get_question())
    def set_question(self, value: str) -> None: self.set_field(NoteFields.Vocab.question, value)

    def get_answer(self) -> str:
        return self.get_user_answer() or self.get_field(NoteFields.Vocab.source_answer)

    def _set_source_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_answer, value)

    def get_user_answer(self) -> str: return self.get_field(NoteFields.Vocab.user_answer)
    def set_user_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.user_answer, value)

    def get_related_similar_meaning(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.Related_similar_meaning)))
    def add_related_similar_meaning(self, new_similar: str, _is_recursive_call: bool = False) -> None:
        similar_vocab_questions = self.get_related_similar_meaning()
        similar_vocab_questions.add(new_similar)

        self.set_field(NoteFields.Vocab.Related_similar_meaning, ", ".join(similar_vocab_questions))

        if not _is_recursive_call:
            from ankiutils import app
            for similar in app.col().vocab.with_question(new_similar):
                similar.add_related_similar_meaning(self.get_question(), _is_recursive_call=True)

    def get_related_derived_from(self) -> str: return self.get_field(NoteFields.Vocab.Related_derived_from)
    def set_related_derived_from(self, value: str) -> None: self.set_field(NoteFields.Vocab.Related_derived_from, value)

    def get_related_ergative_twin(self) -> str: return self.get_field(NoteFields.Vocab.Related_ergative_twin)
    def set_related_ergative_twin(self, value: str) -> None:
        self.set_field(NoteFields.Vocab.Related_ergative_twin, value)

        from ankiutils import app
        for twin in app.col().vocab.with_question(value):
            twin.set_field(NoteFields.Vocab.Related_ergative_twin, self.get_question())

    def get_related_confused_with(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.Related_confused_with)))
    def add_related_confused_with(self, new_confused_with: str) -> None:
        confused_with = self.get_related_confused_with()
        confused_with.add(new_confused_with)
        self.set_field(NoteFields.Vocab.Related_confused_with, ", ".join(confused_with))

    def get_speech_type(self) -> str: return self.get_field(NoteFields.Vocab.Speech_Type)
    def set_speech_type(self, value: str) -> None: self.set_field(NoteFields.Vocab.Speech_Type, value)
    def get_speech_types(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.Speech_Type)))

    _transitive_string_values = ["transitive", "transitive verb"]
    _intransitive_string_values = ["intransitive", "intransitive verb"]
    def is_transitive(self) -> bool: return any(val for val in self._transitive_string_values if val in self.get_speech_types())
    def is_intransitive(self) -> bool: return any(val for val in self._intransitive_string_values if val in self.get_speech_types())

    def get_context_jp(self) -> str: return ex_str.strip_html_markup(self.get_field(NoteFields.Vocab.Context_jp))
    def set_context_jp(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp, value)

    def get_context_jp_audio(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_audio)

    def get_context_en(self) -> str: return self.get_field(NoteFields.Vocab.Context_en)
    def set_context_en(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en, value)

    def get_context_jp_2(self) -> str: return ex_str.strip_html_markup(self.get_field(NoteFields.Vocab.Context_jp_2))
    def set_context_jp_2(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp_2, value)

    def get_context_jp_2_audio(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_2_audio)

    def get_context_en_2(self) -> str: return self.get_field(NoteFields.Vocab.Context_en_2)
    def set_context_en_2(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en_2, value)

    def get_context_jp_3(self) -> str: return ex_str.strip_html_markup(self.get_field(NoteFields.Vocab.Context_jp_3))
    def set_context_jp_3(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp_3, value)

    def get_context_jp_3_audio(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_3_audio)

    def get_context_en_3(self) -> str: return self.get_field(NoteFields.Vocab.Context_en_3)
    def set_context_en_3(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en_3, value)

    def set_meaning_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_mnemonic, value)

    def get_audio_male(self) -> str: return self.get_field(NoteFields.Vocab.Audio_b)
    def set_audio_male(self, value: list[str]) -> None: self.set_field(NoteFields.Vocab.Audio_b, ''.join([f'[sound:{item}]' for item in value]))

    def get_audio_female(self) -> str: return self.get_field(NoteFields.Vocab.Audio_g)
    def set_audio_female(self, value: list[str]) -> None: self.set_field(NoteFields.Vocab.Audio_g, ''.join([f'[sound:{item}]' for item in value]))

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        vocabnote_wanikani_extensions.update_from_wani(self, wani_vocab)

    @staticmethod
    def create_from_wani_vocabulary(wani_vocab: models.Vocabulary) -> None:
        return vocabnote_wanikani_extensions.create_from_wani_vocabulary(wani_vocab)
