class MyNoteFields:
    Vocab1 = "__vocab1"
    Vocab2 = "__vocab2"
    Vocab3 = "__vocab3"
    Vocab4 = "__vocab4"
    Vocab5 = "__vocab5"

class SentenceNoteFields:
    Expression = "Expression"
    Expression__ = "__expression"
    ParsedWords = "ParsedWords"

class Wani:
    class WaniVocabNoteType:
        class Card:
            Reading = "Reading"
            Listening = "Listening"
            Recognition = "Recognition"

    class NoteType:
        Kanji = "WaniKanji"
        Vocab = "WaniVocab"
        Radical = "WaniRadical"

    class NoteFields:
        sort_id = "sort_id"

        subject_id = "subject_id"
        level = "level"
        lesson_position = "lesson_position"
        document_url = "document_url"
        my_learning_order = "my_learning_order"

#        hidden_at = "hidden_at"
#        spaced_repetition_system_id = "spaced_repetition_system_id"
#        created_at = "created_at"
        auxiliary_meanings_whitelist = "auxiliary_meanings_whitelist"
        auxiliary_meanings_blacklist = "auxiliary_meanings_blacklist"

    class RadicalFields:
        Radical = "Radical"
        Radical_Name = "Radical_Name"
        Radical_Meaning = "Radical_Meaning"
        Radical_Icon = "Radical_Icon"
        sort_id = "sort_id"

        amalgamation_subject_ids = "amalgamation_subject_ids"

    class KanjiFields:
        Kanji = "Kanji"
        Kanji_Meaning = "Kanji_Meaning"
        Reading_On = "Reading_On"
        Reading_Kun = "Reading_Kun"
        Radicals = "Radicals"
        Radicals_Icons = "Radicals_Icons"
        Radicals_Names = "Radicals_Names"
        Radicals_Icons_Names = "Radicals_Icons_Names"
        Meaning_Mnemonic = "Meaning_Mnemonic"
        Meaning_Info = "Meaning_Info"
        Reading_Mnemonic = "Reading_Mnemonic"
        Reading_Info = "Reading_Info"
        Override_meaning = "__meaning_Override"
        PrimaryVocab = "__primary_Vocab"
        Audio__ = "__audio"

        Mnemonics_Override = "__mnemonics_Override"

        amalgamation_subject_ids = "amalgamation_subject_ids"
        component_subject_ids = "component_subject_ids"

        Vocabs = "Vocabs"
        VocabsRaw = "VocabsRaw"

    class KanaVocabFields:
        Vocab = "Vocab"
        Vocab_Meaning = "Vocab_Meaning"
        Override_meaning = "__override_meaning"
        Reading = "Reading"
        Speech_Type = "Speech_Type"
        Context_jp = "Context_jp"
        Context_en = "Context_en"
        Context_jp_2 = "Context_jp_2"
        Context_en_2 = "Context_en_2"
        Context_jp_3 = "Context_jp_3"
        Context_en_3 = "Context_en_3"
        Meaning_Exp = "Meaning_Exp"
        Audio_b = "Audio_b"
        Audio_g = "Audio_g"
        sort_id = "sort_id"

        Related_homophones = "Homophones"
        Related_similar_meaning = "__similar_meaning"
        Related_derived_from = "__derivedFrom"
        Related_ergative_twin = "__ergative_twin"
        Related_similarVocab = "__similar_vocab"

    class VocabFields(KanaVocabFields):
        Kanji = "Kanji"
        Kanji_Name = "Kanji_Name"
        Reading_Exp = "Reading_Exp"
        Homophones = "Homophones"
        ParsedTypeOfSpeech = "ParsedTypeOfSpeech"
        Mnemonics_Override = "__override_mnemonic"

        component_subject_ids = "component_subject_ids"


class Mine:
    class Tags:
        Sentence = "_sentence"
        Wani = "_wani"
        UsuallyKanaOnly = "_uk"

    class DeckFilters:
        Listen = "*listen*"
        Sentence = "*sentence*"
