from __future__ import annotations

from typing import Callable

from wanikani_api import models
from anki.notes import Note
from note.waninote import WaniNote
from note.note_constants import NoteFields, Mine, NoteTypes
from sysutils import ex_str
from wanikani.wanikani_api_client import WanikaniClient

class KanjiNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def _on_before_flush(self) -> None: self.update_generated_data()

    def tag_readings_in_string(self, vocabulary: str, tagger: Callable[[str], str]) -> str:
        readings = f"{self.get_reading_kun()}, {self.get_reading_on()}"
        readings_list = [s.split(".")[0].strip() for s in (ex_str.strip_html_and_bracket_markup(readings).split(","))]
        readings_list.sort(key=len, reverse=True)
        for reading in readings_list:
            if reading and reading in vocabulary:
                return vocabulary.replace(reading, tagger(reading), 1)
        return vocabulary

    def get_question(self) -> str: return self.get_field(NoteFields.Kanji.question)
    def set_question(self, value: str) -> None: self.set_field(NoteFields.Kanji.question, value)

    def get_answer(self) -> str:
        return self.get_user_answer() or self.get_field(NoteFields.Kanji.source_answer)

    def get_user_answer(self) -> str: return self.get_field(NoteFields.Kanji.user_answer)
    def set_user_answer(self, value: str) -> None: return self.set_field(NoteFields.Kanji.user_answer, value)

    def _set_source_answer(self, value: str) -> None: self.set_field(NoteFields.Kanji.source_answer, value)

    def update_generated_data(self) -> None:
        self.set_field(NoteFields.Kanji.active_answer, self.get_answer())

    def override_meaning_mnemonic(self) -> None:
        if not self.get_user_mnemonic():
            self.set_user_mnemonic("-")

    def restore_meaning_mnemonic(self) -> None:
        if self.get_user_mnemonic() == "-":
            self.set_user_mnemonic("")

    def get_user_mnemonic(self) -> str: return self.get_field(NoteFields.Kanji.user_mnemonic)
    def set_user_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Kanji.user_mnemonic, value)

    def get_reading_on(self) -> str: return self.get_field(NoteFields.Kanji.Reading_On)
    def set_reading_on(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_On, value)

    def get_reading_kun(self) -> str: return self.get_field(NoteFields.Kanji.Reading_Kun)
    def set_reading_kun(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_Kun, value)

    def get_radicals(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_field(NoteFields.Kanji.Radicals))
    def set_radicals(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals, value)

    def get_radicals_icons(self) -> str: return self.get_field(NoteFields.Kanji.Radicals_Icons)
    def set_radicals_icons(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals_Icons, value)

    def get_radical_dependencies_names(self) -> list[str]:
        return ex_str.extract_comma_separated_values(
            self.get_radicals_names()) + ex_str.extract_comma_separated_values(
            self.get_radicals_icons_names())

    def get_radicals_names(self) -> str: return self.get_field(NoteFields.Kanji.Radicals_Names)
    def set_radicals_names(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals_Names, value)

    def get_radicals_icons_names(self) -> str: return self.get_field(NoteFields.Kanji.Radicals_Icons_Names)
    def set_radicals_icons_names(self, value: str) -> None: self.set_field(NoteFields.Kanji.Radicals_Icons_Names, value)

    def get_active_mnemonic(self) -> str:
        return self.get_user_mnemonic() if self.get_user_mnemonic() else self.get_source_meaning_mnemonic()

    def get_source_meaning_mnemonic(self) -> str: return self.get_field(NoteFields.Kanji.Source_Meaning_Mnemonic)
    def set_source_meaning_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Kanji.Source_Meaning_Mnemonic, value)

    def get_meaning_hint(self) -> str: return self.get_field(NoteFields.Kanji.Meaning_Info)
    def set_meaning_hint(self, value: str) -> None: self.set_field(NoteFields.Kanji.Meaning_Info, value if value is not None else "")

    def get_reading_mnemonic(self) -> str: return self.get_field(NoteFields.Kanji.Reading_Mnemonic)
    def set_reading_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_Mnemonic, value)

    def get_reading_hint(self) -> str: return self.get_field(NoteFields.Kanji.Reading_Info)
    def set_reading_hint(self, value: str) -> None: self.set_field(NoteFields.Kanji.Reading_Info, value if value is not None else "")

    def get_amalgamation_subject_ids(self) -> str: return self.get_field(NoteFields.Kanji.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Kanji.amalgamation_subject_ids, value)

    def get_component_subject_ids(self) -> str: return self.get_field(NoteFields.Kanji.component_subject_ids)
    def set_component_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Kanji.component_subject_ids, value)

    def get_vocabs(self) -> str: return self.get_field(NoteFields.Kanji.Vocabs)
    def set_vocabs(self, value: str) -> None: self.set_field(NoteFields.Kanji.Vocabs, value)

    def get_vocabs_raw(self) -> list[str]: return self.get_field(NoteFields.Kanji.VocabsRaw).split(",")
    def set_vocabs_raw(self, value: list[str]) -> None: self.set_field(NoteFields.Kanji.VocabsRaw, ",".join(value))

    def get_primary_vocab(self) -> list[str]:
        return [voc for voc in
                (ex_str.strip_html_and_bracket_markup(vocab).strip() for vocab in self.get_field(NoteFields.Kanji.PrimaryVocab).split(","))
                if voc]
    def set_primary_vocab(self, value: list[str]) -> None:
        formatted = [self.tag_readings_in_string(voc, lambda read: f"<read>{read}</read>") for voc in value]
        self.set_field(NoteFields.Kanji.PrimaryVocab, ", ".join(formatted))

    def get_primary_vocab_audio(self) -> str: return self.get_field(NoteFields.Kanji.Audio__)
    def set_primary_vocab_audio(self, value: str) -> None: self.set_field(NoteFields.Kanji.Audio__, value)

    def update_from_wani(self, wani_kanji: models.Kanji) -> None:
        super().update_from_wani(wani_kanji)

        self.set_source_meaning_mnemonic(wani_kanji.meaning_mnemonic)
        self.set_meaning_hint(wani_kanji.meaning_hint)

        self.set_reading_mnemonic(wani_kanji.reading_mnemonic)
        self.set_reading_hint(wani_kanji.reading_hint)

        meanings = [f"<primary>{meaning.meaning}</primary>" if meaning.primary else meaning.meaning
                    for meaning in wani_kanji.meanings]

        self._set_source_answer(", ".join(meanings))

        onyomi_readings = [f"<primary>{reading.reading}</primary>" if reading.primary else reading.reading
                           for reading in wani_kanji.readings if reading.type == "onyomi"]

        kunyomi_readings = [f"<primary>{reading.reading}</primary>" if reading.primary else reading.reading
                            for reading in wani_kanji.readings if reading.type == "kunyomi"]

        self.set_reading_on(", ".join(onyomi_readings))
        self.set_reading_kun(", ".join(kunyomi_readings))

        amalgamation_subject_ids = [str(subject_id) for subject_id in wani_kanji.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

        component_subject_ids = [str(subject_id) for subject_id in wani_kanji.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

        client = WanikaniClient.get_instance()
        radicals = [client.get_radical_by_id(int(radical_id)) for radical_id in component_subject_ids]
        radicals_with_characters = [radical for radical in radicals if radical.characters is not None]
        radicals_without_characters = [radical for radical in radicals if radical.characters is None]

        radical_characters = [radical.characters for radical in radicals_with_characters]
        self.set_radicals(", ".join(radical_characters))

        radical_names = [radical.meanings[0].meaning for radical in radicals_with_characters]
        self.set_radicals_names(", ".join(radical_names))

        characterless_radical_names = [radical.meanings[0].meaning for radical in radicals_without_characters]
        self.set_radicals_icons_names(", ".join(characterless_radical_names))

        vocabs = [client.get_vocab_by_id(int(kanji_id)) for kanji_id in amalgamation_subject_ids]
        vocabs.sort(key=lambda voc: (voc.level, voc.lesson_position))
        vocab_html = '''
<div class="vocabList">
    <div>'''

        for vocab in vocabs:
            vocab_html += '''
        <div>{} ({}) {}</div>'''.format(vocab.characters, vocab.readings[0].reading, vocab.meanings[0].meaning)

        vocab_html += '''
    </div>
</div>
'''
        self.set_vocabs(vocab_html)

    @staticmethod
    def create_from_wani_kanji(wani_kanji: models.Kanji) -> None:
        from ankiutils import app
        note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Kanji))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        kanji_note = KanjiNote(note)
        app.anki_collection().addNote(note)
        kanji_note.set_question(wani_kanji.characters)
        kanji_note.update_from_wani(wani_kanji)

    @classmethod
    def create(cls, question: str, answer: str, on_readings: str, kun_reading: str) -> KanjiNote:
        from ankiutils import app
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Kanji))
        note = KanjiNote(backend_note)
        note.set_question(question)
        note.set_user_answer(answer)
        note.set_reading_on(on_readings)
        note.set_reading_kun(kun_reading)
        note.update_generated_data()
        app.anki_collection().addNote(backend_note)
        return note
