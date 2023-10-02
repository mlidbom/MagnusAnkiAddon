from wanikani_api import models
from ankiutils.anki_shim import facade
from anki.notes import Note

from note.kanavocabnote import KanaVocabNote
from sysutils import kana_utils
from sysutils.stringutils import StringUtils
from note.note_constants import NoteFields, Mine, NoteTypes
from wanikani.wanikani_api_client import WanikaniClient


class VocabNote(KanaVocabNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def __repr__(self) -> str: return f"""{self.get_question()}"""

    def get_kanji(self) -> str: return super().get_field(NoteFields.Vocab.Kanji)
    def set_kanji(self, value: str) -> None: super().set_field(NoteFields.Vocab.Kanji, value)

    def get_forms(self) -> set[str]: return set(StringUtils.extract_comma_separated_values(self._get_forms()))
    def set_forms(self, forms: set[str]) -> None: self._set_forms(", ".join([form.strip() for form in forms]))
    def _get_forms(self) -> str: return super().get_field(NoteFields.Vocab.Forms)
    def _set_forms(self, value: str) -> None: super().set_field(NoteFields.Vocab.Forms, value)

    def update_generated_data(self) -> None:
        from parsing.jamdict_extensions.dict_lookup import DictLookup

        super().update_generated_data()

        question = self.get_question().strip()
        readings = ",".join(self.get_readings())

        if question == readings:
            self.set_tag(Mine.Tags.UsuallyKanaOnly)

        if not readings:
            if kana_utils.is_only_kana(question):
                self.set_readings([question])
                self.set_tag(Mine.Tags.UsuallyKanaOnly)

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

    def extract_kanji(self) -> list[str]:
        clean = StringUtils.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if not kana_utils.is_kana(char)]

    def is_uk(self) -> bool: return self.has_tag(Mine.Tags.UsuallyKanaOnly)

    def get_display_question(self) -> str:
        return self.get_readings()[0] if self.is_uk() else self.get_question()

    def get_kanji_name(self) -> str: return super().get_field(NoteFields.Vocab.Kanji_Name)
    def set_kanji_name(self, value: str) -> None: super().set_field(NoteFields.Vocab.Kanji_Name, value)

    def get_reading_mnemonic(self) -> str: return super().get_field(NoteFields.Vocab.Reading_Exp)
    def set_reading_mnemonic(self, value: str) -> None: super().set_field(NoteFields.Vocab.Reading_Exp, value)

    def get_readings(self) -> list[str]: return [reading.strip() for reading in self._get_reading().split(",")]
    def set_readings(self, readings: list[str]) -> None: self._set_reading(", ".join([reading.strip() for reading in readings]))

    def _get_reading(self) -> str: return super().get_field(NoteFields.IgnoreThisUseVocabInstead.Reading)
    def _set_reading(self, value: str) -> None: super().set_field(NoteFields.IgnoreThisUseVocabInstead.Reading, value)

    def get_component_subject_ids(self) -> str: return super().get_field(NoteFields.Vocab.component_subject_ids)
    def set_component_subject_ids(self, value: str) -> None: super().set_field(NoteFields.Vocab.component_subject_ids, value)

    def override_meaning_mnemonic(self) -> None:
        if not self.get_mnemonics_override():
            self.set_mnemonics_override("-")

    def restore_meaning_mnemonic(self) -> None:
        if self.get_mnemonics_override() == "-":
            self.set_mnemonics_override("")

    def get_mnemonics_override(self) -> str: return super().get_field(NoteFields.Vocab.Mnemonic__)
    def set_mnemonics_override(self, value: str) -> None: super().set_field(NoteFields.Vocab.Mnemonic__, value)

    def get_parsed_type_of_speech(self) -> str: return super().get_field(NoteFields.Vocab.ParsedTypeOfSpeech)
    def set_parsed_type_of_speech(self, value: str) -> None: super().set_field(NoteFields.Vocab.ParsedTypeOfSpeech, value)

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)

        self.set_reading_mnemonic(wani_vocab.reading_mnemonic)

        readings = [reading.reading for reading in wani_vocab.readings]
        self._set_reading(", ".join(readings))

        component_subject_ids = [str(subject_id) for subject_id in wani_vocab.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

        client = WanikaniClient.get_instance()
        kanji_subjects = [client.get_kanji_by_id(kanji_id) for kanji_id in wani_vocab.component_subject_ids]
        kanji_characters = [subject.characters for subject in kanji_subjects]
        self.set_kanji(", ".join(kanji_characters))

        kanji_names = [subject.meanings[0].meaning for subject in kanji_subjects]
        self.set_kanji_name(", ".join(kanji_names))

    @staticmethod
    def create_from_wani_vocabulary(wani_vocab: models.Vocabulary) -> None:
        note = Note(facade.anki_collection(), facade.anki_collection().models.by_name(NoteTypes.Vocab))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        kanji_note = VocabNote(note)
        facade.anki_collection().addNote(note)
        kanji_note._set_question(wani_vocab.characters)
        kanji_note.update_from_wani(wani_vocab)

        #Do not move to update method or we will wipe out local changes made to the context sentences.
        if len(wani_vocab.context_sentences) > 0:
            kanji_note.set_context_en(wani_vocab.context_sentences[0].english)
            kanji_note.set_context_jp(wani_vocab.context_sentences[0].japanese)

        if len(wani_vocab.context_sentences) > 1:
            kanji_note.set_context_en_2(wani_vocab.context_sentences[1].english)
            kanji_note.set_context_jp_2(wani_vocab.context_sentences[1].japanese)

        if len(wani_vocab.context_sentences) > 2:
            kanji_note.set_context_en_3(wani_vocab.context_sentences[2].english)
            kanji_note.set_context_jp_3(wani_vocab.context_sentences[2].japanese)

    def generate_and_set_answer(self) -> None:
        from parsing.jamdict_extensions.dict_lookup import DictLookup
        dict_lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.set_user_answer(generated)


