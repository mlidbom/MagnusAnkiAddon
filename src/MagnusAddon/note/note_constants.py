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
    Sentence = "_japanese_sentence"

    ALL = {Kanji, Vocab, Sentence}

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

    class Kanji(Slots):
        question = MyNoteFields.question
        active_answer = MyNoteFields.answer
        source_answer = "source_answer"
        user_answer = "__answer"
        Reading_On = "Reading_On"
        Reading_Kun = "Reading_Kun"
        Reading_Nan = "__reading_Nan"
        Radicals = "Radicals"
        Source_Meaning_Mnemonic = "Meaning_Mnemonic"
        Meaning_Info = "Meaning_Info"
        Reading_Mnemonic = "Reading_Mnemonic"
        Reading_Info = "Reading_Info"
        PrimaryVocab = "__primary_Vocab"
        Audio__ = "__audio"

        user_mnemonic = "__mnemonic"
        user_similar_meaning = "__similar_meaning"
        related_confused_with = "__confused_with"

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
        source_mnemonic = "source_mnemonic"
        Audio_b = "Audio_b"
        Audio_g = "Audio_g"
        Audio_TTS = "Audio_TTS"

        Forms = "F"
        source_reading_mnemonic = "source_reading_mnemonic"
        Homophones = "Homophones"
        ParsedTypeOfSpeech = "ParsedTypeOfSpeech"

        component_subject_ids = "component_subject_ids"

f_root = "-::"
f_sentence = f"{f_root}sentence::"
f_kanji = f"{f_root}kanji::"
f_sentence_uses = f"{f_sentence}uses::"
f_vocab = f"{f_root}vocab::"
f_vocab_matching = f"{f_vocab}matching::"
f_vocab_matching_requires = f"{f_vocab_matching}requires::"
f_vocab_matching_forbids = f"{f_vocab_matching}forbids::"
f_vocab_matching_todo = f"{f_vocab_matching}todo::"
f_vocab_matching_uses = f"{f_vocab_matching}uses::"

class Tags(Slots):
    class Sentence:
        class Uses:
            incorrect_matches = f"{f_sentence_uses}incorrect-matches"
            hidden_matches = f"{f_sentence_uses}hidden-matches"

    class Kanji:
        is_radical = f"{f_kanji}is-radical"
        is_radical_purely = f"{f_kanji}is-radical-purely"
        is_radical_silent = f"{f_kanji}is-radical-silent"
        in_vocab_main_form = f"{f_kanji}in-vocab-main-form"
        in_any_vocab_form = f"{f_kanji}in-any-vocab-form"

        with_single_kanji_vocab = f"{f_kanji}single-kanji-vocab"
        with_single_kanji_vocab_with_different_reading = f"{f_kanji}single-kanji-vocab-with-different-reading"
        with_studying_single_kanji_vocab_with_different_reading = f"{f_kanji}studying-single-kanji-vocab-with-different-reading"
        with_no_primary_on_readings = f"{f_kanji}no-primary-on-readings"
        with_no_primary_readings = f"{f_kanji}no-primary-readings"
        with_studying_vocab = f"{f_kanji}studying-vocab"
        with_vocab_with_primary_on_reading = f"{f_kanji}has-vocab-with-primary-on-reading"
        with_studying_vocab_with_primary_on_reading = f"{f_kanji}studying-vocab-with-primary-on-reading"

        has_studying_vocab_with_no_matching_primary_reading = f"{f_kanji}has-studying-vocab-with-no-matching-primary-reading"
        has_studying_vocab_for_each_primary_reading = f"{f_kanji}has-studying-vocab-for-each-primary-reading"
        has_primary_reading_with_no_studying_vocab = f"{f_kanji}has-primary-reading-with-no-studying-vocab"
        has_non_primary_on_reading_vocab = f"{f_kanji}has-non-primary-on-reading-vocab"
        has_non_primary_on_reading_vocab_with_only_known_kanji = f"{f_kanji}has-non-primary-on-reading-vocab-with-only-known-kanji"

    class Vocab:
        has_no_studying_sentences = f"{f_vocab}has-no-studying-sentences"
        question_overrides_form = f"{f_vocab}question-overrides-form"

        class Matching:
            yield_to_upcoming_compounds = f"{f_vocab_matching}yield-to-upcoming-compounds"
            is_inflecting_word = f"{f_vocab_matching}is-inflecting-word"

            class Requires:
                a_stem = f"{f_vocab_matching_requires}a-stem"
                e_stem = f"{f_vocab_matching_requires}e-stem"
                sentence_end = f"{f_vocab_matching_requires}sentence-end"
                exact_match = f"{f_vocab_matching_requires}exact-match"

            class Forbids:
                a_stem = f"{f_vocab_matching_forbids}a-stem"

            is_strictly_suffix = f"{f_vocab_matching}is-strictly-suffix"

            class Todo:
                with_preceding_vowel = f"{f_vocab_matching_todo}match-with-preceding-vowel"

            class Uses:
                prefer_over_base = f"{f_vocab_matching_uses}prefer-over-base"
                prefix_is_not = f"{f_vocab_matching_uses}prefix-is-not"
                required_prefix = f"{f_vocab_matching_uses}required-prefix"
                surface_is_not = f"{f_vocab_matching_uses}surface-is-not"

    system_tags = {Vocab.Matching.is_inflecting_word}

    priority_folder = f"{f_root}priority::"

    source_folder = "source::"

    Wani = f"{source_folder}wani"
    wani_sentence_current = f"{Wani}::current"
    wani_sentence_removed_on_wani = f"{Wani}::removed"

    immersion_kit = f"{source_folder}immersion_kit"

    DisableKanaOnly = "_disable_uk"
    UsuallyKanaOnly = "_uk"
    TTSAudio = "_tts_audio"

class Mine(Slots):
    app_name = "JA-Studio"
    app_still_loading_message = f"{app_name} still loading....."
    VocabPrefixSuffixMarker = "〜"
