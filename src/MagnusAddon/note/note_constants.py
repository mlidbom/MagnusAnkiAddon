# noinspection PyUnusedName
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
    configuration = "__configuration"

class CardTypes:
    reading = "Reading"
    listening = "Listening"

class NoteTypes:
    immersion_kit = "Immersion Kit Sentence"
    Kanji = "_Kanji"
    Vocab = "_Vocab"
    Radical = "_Radical"
    Sentence = "_japanese_sentence"

    ALL = {Kanji, Vocab, Radical, Sentence}

class NoteFields:
    note_id = "nid"
    class VocabNoteType:
        class Card:
            Reading = CardTypes.reading
            Listening = CardTypes.listening

    class SentencesNoteType:
        class Card:
            Reading = CardTypes.reading
            Listening = CardTypes.listening

    class WaniCommon:
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
        related_confused_with = "__confused_with"

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


        base_folder = "-::"

        inflecting_word = f"{base_folder}inflecting-word"
        requires_exact_match = f"{base_folder}requires-exact-match"
        question_overrides_form = f"{base_folder}question-overrides-form"
        requires_a_stem = f"{base_folder}requires-a-stem"
        requires_e_stem = f"{base_folder}requires-e-stem"

        kanji_folder = f"{base_folder}kanji::"
        kanji_is_radical = f"{kanji_folder}is-radical"
        kanji_is_radical_purely = f"{kanji_folder}is-radical-purely"
        kanji_is_radical_silent = f"{kanji_folder}is-radical-silent"
        kanji_with_single_kanji_vocab = f"{kanji_folder}single-kanji-vocab"
        kanji_in_vocab_main_form = f"{kanji_folder}in-vocab-main-form"
        kanji_in_any_vocab_form = f"{kanji_folder}in-any-vocab-form"
        kanji_with_single_kanji_vocab_with_different_reading = f"{kanji_folder}single-kanji-vocab-with-different-reading"
        kanji_with_studying_single_kanji_vocab_with_different_reading = f"{kanji_folder}studying-single-kanji-vocab-with-different-reading"
        kanji_with_no_primary_on_readings = f"{kanji_folder}no-primary-on-readings"
        kanji_with_no_primary_readings = f"{kanji_folder}no-primary-readings"
        kanji_with_studying_vocab = f"{kanji_folder}studying-vocab"
        kanji_with_vocab_with_primary_on_reading = f"{kanji_folder}has-vocab-with-primary-on-reading"
        kanji_with_studying_vocab_with_primary_on_reading = f"{kanji_folder}studying-vocab-with-primary-on-reading"
        kanji_has_studying_vocab_with_no_matching_primary_reading = f"{kanji_folder}has-studying-vocab-with-no-matching-primary-reading"
        kanji_has_studying_vocab_for_each_primary_reading = f"{kanji_folder}has-studying-vocab-for-each-primary-reading"
        kanji_has_primary_reading_with_no_studying_vocab = f"{kanji_folder}has-primary-reading-with-no-studying-vocab"
        kanji_has_non_primary_on_reading_vocab = f"{kanji_folder}has-non-primary-on-reading-vocab"
        kanji_has_non_primary_on_reading_vocab_with_only_known_kanji = f"{kanji_folder}has-non-primary-on-reading-vocab-with-only-known-kanji"

        vocab_folder = f"{base_folder}vocab::"
        vocab_has_no_studying_sentences = f"{vocab_folder}has-no-studying-sentences"


        priority_folder = f"{base_folder}priority::"

        source_folder = f"source::"

        Wani = f"{source_folder}wani"
        wani_level = f"{Wani}::level::"
        wani_sentence_current = f"{Wani}::current"
        wani_sentence_removed_on_wani = f"{Wani}::removed"

        immersion_kit = f"{source_folder}immersion_kit"



        DisableKanaOnly = "_disable_uk"
        UsuallyKanaOnly = "_uk"
        TTSAudio = "_tts_audio"

        system_tags = {inflecting_word}

