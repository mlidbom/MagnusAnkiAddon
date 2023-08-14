from typing import Callable

from _lib.wanikani_api import models
from anki.notes import Note
from aqt import mw

from sysutils.utils import StringUtils
from note.waninote import WaniNote
from wanikani.wani_constants import Wani, Mine
from wanikani.wanikani_api_client import WanikaniClient


class WaniKanjiNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def tag_readings_in_string(self, vocabulary: str, tagger: Callable[[str], str]) -> str:
        readings = f"{self.get_reading_kun()}, {self.get_reading_on()}"
        readings_list = [s.split(".")[0].strip() for s in (StringUtils.strip_markup(readings).split(","))]
        readings_list.sort(key=len, reverse=True)
        for reading in readings_list:
            if reading and reading in vocabulary:
                return vocabulary.replace(reading, tagger(reading), 1)
        return vocabulary

    def get_kanji(self) -> str: return super().get_field(Wani.KanjiFields.Kanji)
    def set_kanji(self, value: str) -> None: super().set_field(Wani.KanjiFields.Kanji, value)

    def get_kanji_meaning(self) -> str:
        meaning = self.get_override_meaning()
        if meaning != "":
            return meaning
        return super().get_field(Wani.KanjiFields.Kanji_Meaning)

    def get_override_meaning(self) -> str: return super().get_field(Wani.KanjiFields.Override_meaning)
    def set_override_meaning(self, value: str) -> None: super().set_field(Wani.KanjiFields.Override_meaning, value)

    def override_meaning_mnemonic(self) -> None:
        if not self.get_mnemonics_override():
            self.set_mnemonics_override("-")

    def restore_meaning_mnemonic(self) -> None:
        if self.get_mnemonics_override() == "-":
            self.set_mnemonics_override("")

    def get_mnemonics_override(self) -> str: return super().get_field(Wani.KanjiFields.Mnemonics_Override)
    def set_mnemonics_override(self, value: str) -> None: super().set_field(Wani.KanjiFields.Mnemonics_Override, value)

    def set_kanji_meaning(self, value: str) -> None: super().set_field(Wani.KanjiFields.Kanji_Meaning, value)

    def get_reading_on(self) -> str: return super().get_field(Wani.KanjiFields.Reading_On)
    def set_reading_on(self, value: str) -> None: super().set_field(Wani.KanjiFields.Reading_On, value)

    def get_reading_kun(self) -> str: return super().get_field(Wani.KanjiFields.Reading_Kun)
    def set_reading_kun(self, value: str) -> None: super().set_field(Wani.KanjiFields.Reading_Kun, value)

    def get_radicals(self) -> str: return super().get_field(Wani.KanjiFields.Radicals)
    def set_radicals(self, value: str) -> None: super().set_field(Wani.KanjiFields.Radicals, value)

    def get_radicals_icons(self) -> str: return super().get_field(Wani.KanjiFields.Radicals_Icons)
    def set_radicals_icons(self, value: str) -> None: super().set_field(Wani.KanjiFields.Radicals_Icons, value)

    def get_radicals_names(self) -> str: return super().get_field(Wani.KanjiFields.Radicals_Names)
    def set_radicals_names(self, value: str) -> None: super().set_field(Wani.KanjiFields.Radicals_Names, value)

    def get_radicals_icons_names(self) -> str: return super().get_field(Wani.KanjiFields.Radicals_Icons_Names)
    def set_radicals_icons_names(self, value: str) -> None: super().set_field(Wani.KanjiFields.Radicals_Icons_Names, value)

    def get_meaning_mnemonic(self) -> str: return super().get_field(Wani.KanjiFields.Meaning_Mnemonic)
    def set_meaning_mnemonic(self, value: str) -> None: super().set_field(Wani.KanjiFields.Meaning_Mnemonic, value)

    def get_meaning_hint(self) -> str: return super().get_field(Wani.KanjiFields.Meaning_Info)
    def set_meaning_hint(self, value: str) -> None: super().set_field(Wani.KanjiFields.Meaning_Info, value if value is not None else "")

    def get_reading_mnemonic(self) -> str: return super().get_field(Wani.KanjiFields.Reading_Mnemonic)
    def set_reading_mnemonic(self, value: str) -> None: super().set_field(Wani.KanjiFields.Reading_Mnemonic, value)

    def get_reading_hint(self) -> str: return super().get_field(Wani.KanjiFields.Reading_Info)
    def set_reading_hint(self, value: str) -> None: super().set_field(Wani.KanjiFields.Reading_Info, value if value is not None else "")

    def get_amalgamation_subject_ids(self) -> str: return super().get_field(Wani.KanjiFields.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: super().set_field(Wani.KanjiFields.amalgamation_subject_ids, value)

    def get_component_subject_ids(self) -> str: return super().get_field(Wani.KanjiFields.component_subject_ids)
    def set_component_subject_ids(self, value: str) -> None: super().set_field(Wani.KanjiFields.component_subject_ids, value)

    def get_vocabs(self) -> str: return super().get_field(Wani.KanjiFields.Vocabs)
    def set_vocabs(self, value: str) -> None: super().set_field(Wani.KanjiFields.Vocabs, value)

    def get_vocabs_raw(self) -> list[str]: return super().get_field(Wani.KanjiFields.VocabsRaw).split(",")
    def set_vocabs_raw(self, value: list[str]) -> None: super().set_field(Wani.KanjiFields.VocabsRaw, ",".join(value))

    def get_primary_vocab(self) -> str: return super().get_field(Wani.KanjiFields.PrimaryVocab)
    def set_primary_vocab(self, value: str) -> None: super().set_field(Wani.KanjiFields.PrimaryVocab, value)

    def get_primary_vocab_audio(self) -> str: return super().get_field(Wani.KanjiFields.PrimaryVocabAudio)
    def set_primary_vocab_audio(self, value: str) -> None: super().set_field(Wani.KanjiFields.PrimaryVocabAudio, value)

    def update_from_wani(self, wani_kanji: models.Kanji):
        super().update_from_wani(wani_kanji)

        self.set_meaning_mnemonic(wani_kanji.meaning_mnemonic)
        self.set_meaning_hint(wani_kanji.meaning_hint)

        self.set_reading_mnemonic(wani_kanji.reading_mnemonic)
        self.set_reading_hint(wani_kanji.reading_hint)

        meanings = [f"<primary>{meaning.meaning}</primary>" if meaning.primary else meaning.meaning
                    for meaning in wani_kanji.meanings]

        self.set_kanji_meaning(", ".join(meanings))

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
    def create_from_wani_kanji(wani_kanji: models.Kanji):
        note = Note(mw.col, mw.col.models.byName(Wani.NoteType.Kanji))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        kanji_note = WaniKanjiNote(note)
        mw.col.addNote(note)
        kanji_note.set_kanji(wani_kanji.characters)
        kanji_note.update_from_wani(wani_kanji)
