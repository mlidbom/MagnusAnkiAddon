from anki.notes import Note
from aqt import mw

from wanikani_api import models
from .wani_constants import *
from .wanikani_api_client import WanikaniClient


class WaniNote:
    def __init__(self, note: Note):
        self._note = note

    def _assert_field_exists(self, field_name: str):
        if self._note[field_name] is None:
            raise ValueError("No field named:" + field_name)

    def _get_field(self, field_name: str) -> str:
        self._assert_field_exists(field_name)
        return self._note[field_name]

    def _set_field(self, field_name: str, value: str) -> None:
        self._assert_field_exists(field_name)
        self._note[field_name] = value
        self._note.flush()

    def get_level_tag(self) -> int:
        level_tag = [level for level in self._note.tags if level.startswith('level')][0]
        level_int = int(level_tag[5:])
        return level_int

    def set_level_tag(self, new_level: int) -> None:
        level_tags = [level for level in self._note.tags if level.startswith('level')]
        for level in level_tags:
            self._note.remove_tag(level)
        self._note.add_tag("level{:02d}".format(new_level))
        self._note.flush()

    def get_note_type_name(self) -> str:
        # noinspection PyProtectedMember
        return self._note._note_type['name']  # Todo: find how to do this without digging into protected members

    def get_sort_id(self): return self._get_field(Wani.NoteFields.sort_id)
    def set_sort_id(self, value: str) -> None: self._set_field(Wani.NoteFields.sort_id, value)

    def get_subject_id(self) -> int: return int(self._get_field(Wani.NoteFields.subject_id))
    def set_subject_id(self, value: int) -> None: self._set_field(Wani.NoteFields.subject_id, str(value))

    def get_lesson_position(self) ->int: return int(self._get_field(Wani.NoteFields.lesson_position))
    def set_lesson_position(self, value: int) -> None:
        current_position = self._get_field(Wani.NoteFields.lesson_position)

        # Wani api does some veird stuff sometimes returning 0 as lesson positions for many subjects.
        # Possibly the ones in the current level or currently being studied.
        # Anyway, we do NOT want to overwrite valid lesson positions with zeroes!
        if value > 0:
            self._set_field(Wani.NoteFields.lesson_position, str(value))
        else:
            if current_position == "0" or current_position == "" or current_position is None:
                self._set_field(Wani.NoteFields.lesson_position, str(value))
            else:
                print("Ignoring 0 as value for lesson_position for subject: {}".format(self.get_subject_id()))


    def get_my_learning_order(self) ->str: return self._get_field(Wani.NoteFields.my_learning_order)
    def _set_my_learning_order(self, value: str) -> None: self._set_field(Wani.NoteFields.my_learning_order, value)

    def get_document_url(self) -> str: return self._get_field(Wani.NoteFields.document_url)
    def set_document_url(self, value: str) -> None: self._set_field(Wani.NoteFields.document_url, value)

    def get_level(self) -> int: return int(self._get_field(Wani.NoteFields.level))
    def set_level(self, value: int) -> None:
        self.set_level_tag(value)
        self._set_field(Wani.NoteFields.level, str(value))

    def update_from_wani(self, wani_model: models.Subject):
        self.set_level(wani_model.level)
        self.set_subject_id(wani_model.id)
        self.set_lesson_position(wani_model.lesson_position)
        self.set_document_url(wani_model.document_url)

        my_learning_order = "level:{:02d}-lesson_position:{:03d}".format(self.get_level(), self.get_lesson_position())
        self._set_my_learning_order(my_learning_order)

    def delete(self):
        mw.col.remNotes([self._note.id])
        mw.col.save()

    def card_ids(self):
        return self._note.card_ids()

class WaniKanjiNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_kanji(self): return super()._get_field(Wani.KanjiFields.Kanji)
    def set_kanji(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Kanji, value)

    def get_kanji_meaning(self): return super()._get_field(Wani.KanjiFields.Kanji_Meaning)
    def set_kanji_meaning(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Kanji_Meaning, value)

    def get_reading_on(self): return super()._get_field(Wani.KanjiFields.Reading_On)
    def set_reading_on(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Reading_On, value)

    def get_reading_kun(self): return super()._get_field(Wani.KanjiFields.Reading_Kun)
    def set_reading_kun(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Reading_Kun, value)

    def get_radicals(self): return super()._get_field(Wani.KanjiFields.Radicals)
    def set_radicals(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals, value)

    def get_radicals_icons(self): return super()._get_field(Wani.KanjiFields.Radicals_Icons)
    def set_radicals_icons(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals_Icons, value)

    def get_radicals_names(self): return super()._get_field(Wani.KanjiFields.Radicals_Names)
    def set_radicals_names(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals_Names, value)

    def get_radicals_icons_names(self): return super()._get_field(Wani.KanjiFields.Radicals_Icons_Names)
    def set_radicals_icons_names(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals_Icons_Names,
                                                                               value)
    def get_meaning_mnemonic(self): return super()._get_field(Wani.KanjiFields.Meaning_Mnemonic)
    def set_meaning_mnemonic(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Meaning_Mnemonic, value)

    def get_meaning_hint(self): return super()._get_field(Wani.KanjiFields.Meaning_Info)
    def set_meaning_hint(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Meaning_Info,
                                                                       value if value is not None else "")

    def get_reading_mnemonic(self): return super()._get_field(Wani.KanjiFields.Reading_Mnemonic)
    def set_reading_mnemonic(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Reading_Mnemonic, value)

    def get_reading_hint(self): return super()._get_field(Wani.KanjiFields.Reading_Info)
    def set_reading_hint(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Reading_Info,
                                                                       value if value is not None else "")

    def get_amalgamation_subject_ids(self): return super()._get_field(Wani.KanjiFields.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: super()._set_field(Wani.KanjiFields.amalgamation_subject_ids, value)

    def get_component_subject_ids(self): return super()._get_field(Wani.KanjiFields.component_subject_ids)
    def set_component_subject_ids(self, value: str) -> None: super()._set_field(Wani.KanjiFields.component_subject_ids, value)

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

        amalgamation_subject_ids = [str(id) for id in wani_kanji.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

        component_subject_ids = [str(id) for id in wani_kanji.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

    def create_from_wani_kanji(wani_kanji: models.Kanji):
        note = Note(mw.col, mw.col.models.byName(Wani.NoteType.Kanji))
        note.add_tag("__imported")
        kanji_note = WaniKanjiNote(note)
        mw.col.addNote(note)
        kanji_note.set_kanji(wani_kanji.characters)
        kanji_note.update_from_wani(wani_kanji)


class WaniKanaVocabNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_vocab(self): return super()._get_field(Wani.KanaVocabFields.Vocab)
    def set_vocab(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Vocab, value)

    def get_vocab_meaning(self): return super()._get_field(Wani.KanaVocabFields.Vocab_Meaning)
    def set_vocab_meaning(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Vocab_Meaning, value)

    def get_speech_type(self): return super()._get_field(Wani.KanaVocabFields.Speech_Type)
    def set_speech_type(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Speech_Type, value)

    def get_context_jp(self): return super()._get_field(Wani.KanaVocabFields.Context_jp)
    def set_context_jp(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Context_jp, value)

    def get_context_en(self): return super()._get_field(Wani.KanaVocabFields.Context_en)
    def set_context_en(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Context_en, value)

    def get_context_jp_2(self): return super()._get_field(Wani.KanaVocabFields.Context_jp_2)
    def set_context_jp_2(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Context_jp_2, value)

    def get_context_en_2(self): return super()._get_field(Wani.KanaVocabFields.Context_en_2)
    def set_context_en_2(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Context_en_2, value)

    def get_context_jp_3(self): return super()._get_field(Wani.KanaVocabFields.Context_jp_3)
    def set_context_jp_3(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Context_jp_3, value)

    def get_context_en_3(self): return super()._get_field(Wani.KanaVocabFields.Context_en_3)
    def set_context_en_3(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Context_en_3, value)

    def get_meaning_mnemonic(self): return super()._get_field(Wani.KanaVocabFields.Meaning_Exp)
    def set_meaning_mnemonic(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Meaning_Exp, value)

    def get_audio_male(self): return super()._get_field(Wani.KanaVocabFields.Audio_b)
    def set_audio_male(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Audio_b,
                                                                     "[sound:{}]".format(value))

    def get_audio_female(self): return super()._get_field(Wani.KanaVocabFields.Audio_g)
    def set_audio_female(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Audio_g,
                                                                       "[sound:{}]".format(value))

    def is_wani_vocab(self) -> bool:
        return Mine.Tags.Wani in self._note.tags

    def update_from_wani(self, wani_vocab: models.Vocabulary):
        super().update_from_wani(wani_vocab)

        self.set_meaning_mnemonic(wani_vocab.meaning_mnemonic)

        meanings = ', '.join(str(meaning.meaning) for meaning in wani_vocab.meanings)
        self.set_vocab_meaning(meanings)

        self.set_speech_type(", ".join(wani_vocab.parts_of_speech))

        if len(wani_vocab.context_sentences) > 0:
            self.set_context_en(wani_vocab.context_sentences[0].english)
            self.set_context_jp(wani_vocab.context_sentences[0].japanese)

        if len(wani_vocab.context_sentences) > 1:
            self.set_context_en_2(wani_vocab.context_sentences[1].english)
            self.set_context_jp_2(wani_vocab.context_sentences[1].japanese)

        if len(wani_vocab.context_sentences) > 2:
            self.set_context_en_3(wani_vocab.context_sentences[2].english)
            self.set_context_jp_3(wani_vocab.context_sentences[2].japanese)


class WaniVocabNote(WaniKanaVocabNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_kanji(self): return super()._get_field(Wani.VocabFields.Kanji)
    def set_kanji(self, value: str) -> None: super()._set_field(Wani.VocabFields.Kanji, value)

    def get_kanji_name(self): return super()._get_field(Wani.VocabFields.Kanji_Name)
    def set_kanji_name(self, value: str) -> None: super()._set_field(Wani.VocabFields.Kanji_Name, value)

    def get_reading_mnemonic(self): return super()._get_field(Wani.VocabFields.Reading_Exp)
    def set_reading_mnemonic(self, value: str) -> None: super()._set_field(Wani.VocabFields.Reading_Exp, value)

    def get_reading(self): return super()._get_field(Wani.KanaVocabFields.Reading)
    def set_reading(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Reading, value)

    def get_component_subject_ids(self): return super()._get_field(Wani.VocabFields.component_subject_ids)
    def set_component_subject_ids(self, value: str) -> None: super()._set_field(Wani.VocabFields.component_subject_ids, value)

    def update_from_wani(self, wani_vocab: models.Vocabulary):
        super().update_from_wani(wani_vocab)

        self.set_reading_mnemonic(wani_vocab.reading_mnemonic)

        readings = [reading.reading for reading in wani_vocab.readings]
        self.set_reading(", ".join(readings))

        component_subject_ids = [str(id) for id in wani_vocab.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

        client = WanikaniClient.get_instance()
        kanji_subjects = [client.get_kanji_by_id(kanji_id) for kanji_id in wani_vocab.component_subject_ids]
        kanji_characters = [subject.characters for subject in kanji_subjects]
        self.set_kanji(", ".join(kanji_characters))

        kanji_names = [subject.meanings[0].meaning for subject in kanji_subjects]
        self.set_kanji_name(", ".join(kanji_names))

    def create_from_wani_vocabulary(wani_vocabulary: models.Vocabulary):
        note = Note(mw.col, mw.col.models.byName(Wani.NoteType.Vocab))
        note.add_tag("__imported")
        kanji_note = WaniVocabNote(note)
        mw.col.addNote(note)
        kanji_note.set_vocab(wani_vocabulary.characters)
        kanji_note.update_from_wani(wani_vocabulary)


class WaniRadicalNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_radical_name(self): return super()._get_field(Wani.RadicalFields.Radical_Name)
    def set_radical_name(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical_Name, value)

    def get_radical(self): return super()._get_field(Wani.RadicalFields.Radical)
    def set_radical(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical, value)

    def get_meaning_mnemonic(self): return super()._get_field(Wani.RadicalFields.Radical_Meaning)
    def set_meaning_mnemonic(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical_Meaning, value)

    def get_radical_icon(self): return super()._get_field(Wani.RadicalFields.Radical_Icon)
    def set_radical_icon(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical_Icon, value)

    def get_amalgamation_subject_ids(self): return super()._get_field(Wani.RadicalFields.amalgamation_subject_ids)
    def set_amalgamation_subject_ids(self, value: str) -> None: super()._set_field(Wani.RadicalFields.amalgamation_subject_ids, value)

    def update_from_wani(self, wani_radical: models.Radical):
        super().update_from_wani(wani_radical)
        self.set_meaning_mnemonic(wani_radical.meaning_mnemonic)

        amalgamation_subject_ids = [str(id) for id in  wani_radical.amalgamation_subject_ids]
        self.set_amalgamation_subject_ids(", ".join(amalgamation_subject_ids))

        self.set_level(wani_radical.level)

    def create_from_wani_radical(wani_radical: models.Radical):
        note = Note(mw.col, mw.col.models.byName(Wani.NoteType.Radical))
        note.add_tag("__imported")
        radical_note = WaniRadicalNote(note)
        mw.col.addNote(note)
        radical_note.set_radical(wani_radical.characters)
        radical_note.update_from_wani(wani_radical)
