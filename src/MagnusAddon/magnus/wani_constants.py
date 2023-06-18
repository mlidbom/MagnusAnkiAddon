class Wani:
    class NoteType:
        Kanji = "WaniKanji"
        Vocab = "WaniVocab"
        Radical = "WaniRadical"

    class RadicalFields:
        Radical = "Radical"
        Radical_Name = "Radical_Name"
        Radical_Meaning = "Radical_Meaning"
        Radical_Icon = "Radical_Icon"
        sort_id = "sort_id"

    class KanjiFields:
        Kanji = "Kanji"
        Kanji_Meaning = "Kanji_Meaning"
        Readings_On = "Readings_On"
        Readings_Kun = "Readings_Kun"
        Radicals = "Radicals"
        Radicals_Icons = "Radicals_Icons"
        Radicals_Names = "Radicals_Names"
        Radicals_Icons_Names = "Radicals_Icons_Names"
        Meaning_Mnemonic = "Meaning_Mnemonic"
        Meaning_Info = "Meaning_Info"
        Reading_Mnemonic = "Reading_Mnemonic"
        Reading_Info = "Reading_Info"
        sort_id = "sort_id"

    class KanaVocabFields:
        Vocab = "Vocab"
        Vocab_Meaning = "Vocab_Meaning"
        Reading = "Reading"
        Speech_Type = "Speech_Type"
        Context_jp = "Context_jp"
        Context_en = "Context_en"
        Context_jp_2 = "Context_jp_2"
        Context_en_2 = "Context_en_2"
        Context_jp_3 = "Context_jp_3"
        Context_en_3 = "Context_en_3"
        Meaning_Exp = "Meaning_Exp"
        Reading_Exp = "Reading_Exp"
        Audio_b = "Audio_b"
        Audio_g = "Audio_g"
        sort_id = "sort_id"

    class VocabFields(KanaVocabFields):
        Kanji = "Kanji"
        Kanji_Name = "Kanji_Name"


class Mine:
    class Tags:
        Sentence = "_sentence"

    class DeckFilters:
        Listen = "*listen*"
        Sentence = "*sentence*"
