from anki.notes import Note

from .wani_constants import *


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

    def get_sort_id(self): return self._get_field(Wani.KanjiFields.sort_id)
    def set_sort_id(self, value: str) -> None: self._set_field(Wani.KanjiFields.sort_id, value)

    def get_note_type_name(self) -> str:
        # noinspection PyProtectedMember
        return self._note._note_type['name']  # Todo: find how to do this without digging into protected members

    def card_ids(self):
        return self._note.card_ids()


class WaniKanjiNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_kanji(self): return super()._get_field(Wani.KanjiFields.Kanji)
    def set_kanji(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Kanji, value)

    def get_kanji_meaning(self): return super()._get_field(Wani.KanjiFields.Kanji_Meaning)
    def set_kanji_meaning(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Kanji_Meaning, value)

    def get_reading_on(self): return super()._get_field(Wani.KanjiFields.Readings_On)
    def set_reading_on(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Readings_On, value)

    def get_reading_kun(self): return super()._get_field(Wani.KanjiFields.Readings_Kun)
    def set_reading_kun(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Readings_Kun, value)

    def get_radicals(self): return super()._get_field(Wani.KanjiFields.Radicals)
    def set_radicals(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals, value)

    def get_radicals_icons(self): return super()._get_field(Wani.KanjiFields.Radicals_Icons)
    def set_radicals_icons(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals_Icons, value)

    def get_radicals_names(self): return super()._get_field(Wani.KanjiFields.Radicals_Names)
    def set_radicals_names(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals_Names, value)

    def get_radicals_icons_names(self): return super()._get_field(Wani.KanjiFields.Radicals_Icons_Names)
    def set_radicals_icons_names(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Radicals_Icons_Names, value)

    def get_meaning_mnemonic(self): return super()._get_field(Wani.KanjiFields.Meaning_Mnemonic)
    def set_meaning_mnemonic(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Meaning_Mnemonic, value)

    def get_meaning_info(self): return super()._get_field(Wani.KanjiFields.Meaning_Info)
    def set_meaning_info(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Meaning_Info, value)

    def get_reading_mnemonic(self): return super()._get_field(Wani.KanjiFields.Reading_Mnemonic)
    def set_reading_mnemonic(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Reading_Mnemonic, value)

    def get_reading_info(self): return super()._get_field(Wani.KanjiFields.Reading_Info)
    def set_reading_info(self, value: str) -> None: super()._set_field(Wani.KanjiFields.Reading_Info, value)


class WaniKanaVocabNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_vocab(self): return super()._get_field(Wani.KanaVocabFields.Vocab)
    def set_vocab(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Vocab, value)

    def get_vocab_meaning(self): return super()._get_field(Wani.KanaVocabFields.Vocab_Meaning)
    def set_vocab_meaning(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Vocab_Meaning, value)

    def get_reading(self): return super()._get_field(Wani.KanaVocabFields.Reading)
    def set_reading(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Reading, value)

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

    def get_meaning_exp(self): return super()._get_field(Wani.KanaVocabFields.Meaning_Exp)
    def set_meaning_exp(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Meaning_Exp, value)

    def get_reading_exp(self): return super()._get_field(Wani.KanaVocabFields.Reading_Exp)
    def set_reading_exp(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Reading_Exp, value)

    def get_audio_b(self): return super()._get_field(Wani.KanaVocabFields.Audio_b)
    def set_audio_b(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Audio_b, value)

    def get_audio_g(self): return super()._get_field(Wani.KanaVocabFields.Audio_g)
    def set_audio_g(self, value: str) -> None: super()._set_field(Wani.KanaVocabFields.Audio_g, value)


class WaniVocabNote(WaniKanaVocabNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_kanji(self): return super()._get_field(Wani.VocabFields.Kanji)
    def set_kanji(self, value: str) -> None: super()._set_field(Wani.VocabFields.Kanji, value)

    def get_kanji_name(self): return super()._get_field(Wani.VocabFields.Kanji_Name)
    def set_kanji_name(self, value: str) -> None: super()._set_field(Wani.VocabFields.Kanji_Name, value)


class WaniRadicalNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_radical_name(self): return super()._get_field(Wani.RadicalFields.Radical_Name)
    def set_radical_name(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical_Name, value)

    def get_radical(self): return super()._get_field(Wani.RadicalFields.Radical)
    def set_radical(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical, value)

    def get_radical_meaning(self): return super()._get_field(Wani.RadicalFields.Radical_Meaning)
    def set_radical_meaning(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical_Meaning, value)

    def get_radical_icon(self): return super()._get_field(Wani.RadicalFields.Radical_Icon)
    def set_radical_icon(self, value: str) -> None: super()._set_field(Wani.RadicalFields.Radical_Icon, value)
