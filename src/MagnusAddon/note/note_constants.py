# noinspection PyUnusedName
from __future__ import annotations

from autoslot import Slots


class Builtin(Slots):
    # noinspection PyUnusedName
    Tag = "tag"
    Note = "note"
    Deck = "deck"
    Card = "card"

class MyNoteFields(Slots):
    question = "Q"
    answer = "A"

class ImmersionKitSentenceNoteFields(Slots):
    audio = "Audio Sentence"
    id = "ID"
    screenshot = "Screenshot"
    reading = "Reading"
    answer = "English"
    question = "Expression"

class SentenceNoteFields(Slots):
    reading = "Reading"
    id = "ID"
    active_question = MyNoteFields.question
    source_question = "source_question"
    source_comments = "Comments"
    user_comments = "__comments"
    user_comments_long = "__comments_Long"
    user_question = "__question"
    user_answer_analysis = "__answer_analysis"
    active_answer = MyNoteFields.answer
    source_answer = "source_answer"
    user_answer = "__answer"
    parsing_result = "__parsing_result"
    user_excluded_vocab = "__excluded_vocab"
    user_extra_vocab = "__extra_vocab"
    audio = "Audio Sentence"
    screenshot = "Screenshot"
    configuration = "__configuration"

class CardTypes(Slots):
    reading = "Reading"
    listening = "Listening"

class NoteTypes(Slots):
    immersion_kit = "Immersion Kit Sentence"
    Kanji = "_Kanji"
    Vocab = "_Vocab"
    Radical = "_Radical"
    Sentence = "_japanese_sentence"

    ALL = {Kanji, Vocab, Radical, Sentence}

class NoteFields(Slots):
    note_id = "nid"
    class VocabNoteType(Slots):
        class Card(Slots):
            Reading = CardTypes.reading
            Listening = CardTypes.listening

    class SentencesNoteType(Slots):
        class Card(Slots):
            Reading = CardTypes.reading
            Listening = CardTypes.listening

    class WaniCommon(Slots):
        subject_id = "subject_id"
        level = "level"
        lesson_position = "lesson_position"
        document_url = "document_url"
        my_learning_order = "my_learning_order"

        auxiliary_meanings_whitelist = "auxiliary_meanings_whitelist"
        auxiliary_meanings_blacklist = "auxiliary_meanings_blacklist"

    class Radical(Slots):
        question = MyNoteFields.question
        answer = MyNoteFields.answer
        source_mnemonic = "Radical_Meaning"
        Radical_Icon = "Radical_Icon"
        sort_id = "sort_id"

        amalgamation_subject_ids = "amalgamation_subject_ids"

    class Kanji(Slots):
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

    class Vocab(Slots):
        matching_rules = "__matching_rules"
        related_vocab = "__related_vocab"
        sentence_count = "sentence_count"
        question = MyNoteFields.question
        active_answer = MyNoteFields.answer
        source_answer = "source_answer"
        user_answer = "__answer"
        user_compounds = "__compounds"
        user_explanation = "__explanation"
        user_explanation_long = "__explanation_long"
        user_mnemonic = "__mnemonic"
        Reading = "Reading"
        parts_of_speech = "TOS"
        Context_sentence_1_japanese = "Context_jp"
        Context_sentence_1_audio = "Context_jp_audio"
        Context_sentence_1_english = "Context_en"
        Context_sentence_2_japanese = "Context_jp_2"
        Context_sentence_2_english = "Context_en_2"
        Context_sentence_2_audio = "Context_jp_2_audio"
        Context_sentence_3_japanese = "Context_jp_3"
        Context_sentence_3_english = "Context_en_3"
        Context_sentence_3_audio = "Context_jp_3_audio"
        source_mnemonic = "source_mnemonic"
        Audio_b = "Audio_b"
        Audio_g = "Audio_g"
        Audio_TTS = "Audio_TTS"
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

        component_subject_ids = "component_subject_ids"

class Mine(Slots):
    app_name = "JA-Studio"
    app_still_loading_message = f"{app_name} still loading....."
    VocabPrefixSuffixMarker = "〜"
    class Tags(Slots):
        base_folder = "-::"

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
        question_overrides_form = f"{vocab_folder}question-overrides-form"

        vocab_matching_folder = f"{vocab_folder}matching::"
        vocab_matching_is_inflecting_word = f"{vocab_matching_folder}is-inflecting-word"
        vocab_matching_requires_a_stem = f"{vocab_matching_folder}requires-a-stem"
        vocab_matching_requires_e_stem = f"{vocab_matching_folder}requires-e-stem"
        vocab_matching_requires_exact_match = f"{vocab_matching_folder}requires-exact-match"
        vocab_matching_is_strictly_suffix = f"{vocab_matching_folder}is-strictly-suffix"

        vocab_matching_todo_folder = f"{vocab_matching_folder}todo::"
        vocab_matching_todo_with_preceding_vowel = f"{vocab_matching_todo_folder}match-with-preceding-vowel"

        vocab_matching_uses_folder = f"{vocab_matching_folder}uses::"
        vocab_matching_uses_prefer_over_base = f"{vocab_matching_uses_folder}prefer-over-base"
        vocab_matching_uses_prefix_is_not = f"{vocab_matching_uses_folder}prefix-is-not"
        vocab_matching_uses_required_prefix = f"{vocab_matching_uses_folder}required-prefix"
        vocab_matching_uses_surface_is_not = f"{vocab_matching_uses_folder}surface-is-not"

        priority_folder = f"{base_folder}priority::"

        source_folder = "source::"

        Wani = f"{source_folder}wani"
        wani_level = f"{Wani}::level::"
        wani_sentence_current = f"{Wani}::current"
        wani_sentence_removed_on_wani = f"{Wani}::removed"

        immersion_kit = f"{source_folder}immersion_kit"

        DisableKanaOnly = "_disable_uk"
        UsuallyKanaOnly = "_uk"
        TTSAudio = "_tts_audio"

        system_tags = {vocab_matching_is_inflecting_word}
