class Builtin:
    Note = "note"
    Tag = "tag"
    Deck = "deck"
    Card = "card"

class MyNoteFields:
    question = "Q"
    answer = "A"

class ImmersionKitSentenceNoteFields:
    audio = "Audio Sentence"
    id = "ID"
    screenshot = "Screenshot"
    reading = "Reading"
    answer = "English"
    question = "Expression"

class SentenceNoteFields:
    reading = "Reading"
    id = "ID"
    active_question = MyNoteFields.question
    source_question = "source_question"
    user_question = "__question"
    active_answer = MyNoteFields.answer
    source_answer = "source_answer"
    user_answer = "__answer"
    ParsedWords = "ParsedWords"
    user_excluded_vocab = "__excluded_vocab"
    user_extra_vocab = "__extra_vocab"
    audio = "Audio Sentence"
    screenshot = "Screenshot"

class NoteTypes:
    immersion_kit = "Immersion Kit Sentence"
    Kanji = "_Kanji"
    Vocab = "_Vocab"
    Radical = "_Radical"
    Sentence = "_japanese_sentence"

class NoteFields:
    note_id = "nid"
    class VocabNoteType:
        class Card:
            Reading = "Reading"
            Listening = "Listening"

    class SentencesNoteType:
        class Card:
            Reading = "Reading"
            Listening = "Listening"

    class WaniCommon:
        sort_id = "sort_id"

        subject_id = "subject_id"
        level = "level"
        lesson_position = "lesson_position"
        document_url = "document_url"
        my_learning_order = "my_learning_order"

        auxiliary_meanings_whitelist = "auxiliary_meanings_whitelist"
        auxiliary_meanings_blacklist = "auxiliary_meanings_blacklist"

    class Radical:
        question = MyNoteFields.question
        answer = MyNoteFields.answer
        source_mnemonic = "Radical_Meaning"
        user_mnemonic = "__mnemonic"
        Radical_Icon = "Radical_Icon"
        sort_id = "sort_id"

        amalgamation_subject_ids = "amalgamation_subject_ids"

    class Kanji:
        question = MyNoteFields.question
        active_answer = MyNoteFields.answer
        source_answer = "source_answer"
        user_answer = "__answer"
        Reading_On = "Reading_On"
        Reading_Kun = "Reading_Kun"
        Reading_Nan = "__reading_Nan"
        Radicals = "Radicals"
        Radicals_Icons = "Radicals_Icons"
        Radicals_Names = "Radicals_Names"
        Radicals_Icons_Names = "Radicals_Icons_Names"
        Source_Meaning_Mnemonic = "Meaning_Mnemonic"
        Meaning_Info = "Meaning_Info"
        Reading_Mnemonic = "Reading_Mnemonic"
        Reading_Info = "Reading_Info"
        PrimaryVocab = "__primary_Vocab"
        Audio__ = "__audio"

        user_mnemonic = "__mnemonic"
        user_similar_meaning = "__similar_meaning"

        amalgamation_subject_ids = "amalgamation_subject_ids"
        component_subject_ids = "component_subject_ids"

        Vocabs = "Vocabs"
        VocabsRaw = "VocabsRaw"

    class Vocab:
        sentence_count = "sentence_count"
        question = MyNoteFields.question
        active_answer = MyNoteFields.answer
        source_answer = "source_answer"
        user_answer = "__answer"
        user_compounds = "__compounds"
        Reading = "Reading"
        Speech_Type = "TOS"
        Context_jp = "Context_jp"
        Context_jp_audio = "Context_jp_audio"
        Context_en = "Context_en"
        Context_jp_2 = "Context_jp_2"
        Context_en_2 = "Context_en_2"
        Context_jp_2_audio = "Context_jp_2_audio"
        Context_jp_3 = "Context_jp_3"
        Context_en_3 = "Context_en_3"
        Context_jp_3_audio = "Context_jp_3_audio"
        source_mnemonic = "source_mnemonic"
        Audio_b = "Audio_b"
        Audio_g = "Audio_g"
        sort_id = "sort_id"

        Related_similar_meaning = "__similar_meaning"
        Related_derived_from = "__derivedFrom"
        Related_ergative_twin = "__ergative_twin"
        Related_confused_with = "__confused_with"

        Kanji = "Kanji"
        Forms = "F"
        source_reading_mnemonic = "source_reading_mnemonic"
        Homophones = "Homophones"
        ParsedTypeOfSpeech = "ParsedTypeOfSpeech"
        Mnemonic__ = "__mnemonic"

        component_subject_ids = "component_subject_ids"

class Mine:
    VocabPrefixSuffixMarker = "〜"
    class Tags:
        TTSAudio = "_tts_audio"
        high_priority = "_high_priority"
        low_priority = "_low_priority"
        Sentence = "_sentence"
        Wani = "_wani"
        DisableKanaOnly = "_disable_uk"
        UsuallyKanaOnly = "_uk"
