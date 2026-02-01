from __future__ import annotations

from autoslot import Slots
from note.tag import Tag

f_root = "-::"
f_sentence: str = f"{f_root}sentence::"
f_kanji: str = f"{f_root}kanji::"
f_sentence_uses: str = f"{f_sentence}uses::"
f_vocab: str = f"{f_root}vocab::"
f_vocab_matching: str = f"{f_vocab}matching::"
f_vocab_register: str = f"{f_vocab}register::"
f_vocab_matching_requires: str = f"{f_vocab_matching}requires::"
f_vocab_matching_forbids: str = f"{f_vocab_matching}forbids::"
f_vocab_matching_todo: str = f"{f_vocab_matching}todo::"
f_vocab_matching_uses: str = f"{f_vocab_matching}uses::"
f_source = "source::"

class Tags(Slots):
    class Sentence(Slots):
        class Uses(Slots):
            incorrect_matches: Tag = Tag.from_name(f"{f_sentence_uses}incorrect-matches")
            hidden_matches: Tag = Tag.from_name(f"{f_sentence_uses}hidden-matches")

    class Kanji(Slots):
        is_radical: Tag = Tag.from_name(f"{f_kanji}is-radical")
        is_radical_purely: Tag = Tag.from_name(f"{f_kanji}is-radical-purely")
        is_radical_silent: Tag = Tag.from_name(f"{f_kanji}is-radical-silent")
        in_vocab_main_form: Tag = Tag.from_name(f"{f_kanji}in-vocab-main-form")
        in_any_vocab_form: Tag = Tag.from_name(f"{f_kanji}in-any-vocab-form")

        with_single_kanji_vocab: Tag = Tag.from_name(f"{f_kanji}single-kanji-vocab")
        with_single_kanji_vocab_with_different_reading: Tag = Tag.from_name(f"{f_kanji}single-kanji-vocab-with-different-reading")
        with_studying_single_kanji_vocab_with_different_reading: Tag = Tag.from_name(f"{f_kanji}studying-single-kanji-vocab-with-different-reading")
        with_no_primary_on_readings: Tag = Tag.from_name(f"{f_kanji}no-primary-on-readings")
        with_no_primary_readings: Tag = Tag.from_name(f"{f_kanji}no-primary-readings")
        with_studying_vocab: Tag = Tag.from_name(f"{f_kanji}studying-vocab")
        with_vocab_with_primary_on_reading: Tag = Tag.from_name(f"{f_kanji}has-vocab-with-primary-on-reading")
        with_studying_vocab_with_primary_on_reading: Tag = Tag.from_name(f"{f_kanji}studying-vocab-with-primary-on-reading")

        has_studying_vocab_with_no_matching_primary_reading: Tag = Tag.from_name(f"{f_kanji}has-studying-vocab-with-no-matching-primary-reading")
        has_studying_vocab_for_each_primary_reading: Tag = Tag.from_name(f"{f_kanji}has-studying-vocab-for-each-primary-reading")
        has_primary_reading_with_no_studying_vocab: Tag = Tag.from_name(f"{f_kanji}has-primary-reading-with-no-studying-vocab")
        has_non_primary_on_reading_vocab: Tag = Tag.from_name(f"{f_kanji}has-non-primary-on-reading-vocab")
        has_non_primary_on_reading_vocab_with_only_known_kanji: Tag = Tag.from_name(f"{f_kanji}has-non-primary-on-reading-vocab-with-only-known-kanji")

    class Vocab(Slots):
        root: str = f_vocab  # Keep as string for startswith() checks
        has_no_studying_sentences: Tag = Tag.from_name(f"{f_vocab}has-no-studying-sentences")
        question_overrides_form: Tag = Tag.from_name(f"{f_vocab}question-overrides-form")
        is_compositionally_transparent_compound: Tag = Tag.from_name(f"{f_vocab}is-compositionally-transparent-compound")
        is_ichidan_hiding_godan_potential: Tag = Tag.from_name(f"{f_vocab}is-ichidan-hiding-godan-potential")

        class Register(Slots):
            polite: Tag = Tag.from_name(f"{f_vocab_register}polite")
            formal: Tag = Tag.from_name(f"{f_vocab_register}formal")
            humble: Tag = Tag.from_name(f"{f_vocab_register}humble")
            honorific: Tag = Tag.from_name(f"{f_vocab_register}honorific")
            informal: Tag = Tag.from_name(f"{f_vocab_register}informal")
            slang: Tag = Tag.from_name(f"{f_vocab_register}slang")
            rough_masculine: Tag = Tag.from_name(f"{f_vocab_register}rough")
            soft_feminine: Tag = Tag.from_name(f"{f_vocab_register}soft")
            derogatory: Tag = Tag.from_name(f"{f_vocab_register}derogatory")
            vulgar: Tag = Tag.from_name(f"{f_vocab_register}vulgar")
            archaic: Tag = Tag.from_name(f"{f_vocab_register}archaic")
            sensitive: Tag = Tag.from_name(f"{f_vocab_register}sensitive")
            childish: Tag = Tag.from_name(f"{f_vocab_register}childish")
            literary: Tag = Tag.from_name(f"{f_vocab_register}literary")

        class Matching(Slots):
            yield_last_token_to_overlapping_compound: Tag = Tag.from_name(f"{f_vocab_matching}yield-last-token-to-upcoming-compound")
            is_poison_word: Tag = Tag.from_name(f"{f_vocab_matching}is-poison-word")
            is_inflecting_word: Tag = Tag.from_name(f"{f_vocab_matching}is-inflecting-word")

            class Requires(Slots):
                folder_name: str = f_vocab_matching_requires
                masu_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}masu_stem")
                godan: Tag = Tag.from_name(f"{f_vocab_matching_requires}godan")
                ichidan: Tag = Tag.from_name(f"{f_vocab_matching_requires}ichidan")
                irrealis: Tag = Tag.from_name(f"{f_vocab_matching_requires}irrealis")
                preceding_adverb: Tag = Tag.from_name(f"{f_vocab_matching_requires}preceding_adverb")
                past_tense_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}past-tense-stem")
                dictionary_form_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}dictionary_form_stem")
                dictionary_form_prefix: Tag = Tag.from_name(f"{f_vocab_matching_requires}dictionary_form_prefix")
                ichidan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_requires}ichidan_imperative")
                godan_potential: Tag = Tag.from_name(f"{f_vocab_matching_requires}godan_potential")
                godan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_requires}godan_imperative")
                godan_imperative_prefix: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_imperative_prefix")
                te_form_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}te-form-stem")
                te_form_prefix: Tag = Tag.from_name(f"{f_vocab_matching_requires}te-form-prefix")
                sentence_end: Tag = Tag.from_name(f"{f_vocab_matching_requires}sentence-end")
                sentence_start: Tag = Tag.from_name(f"{f_vocab_matching_requires}sentence-start")
                surface: Tag = Tag.from_name(f"{f_vocab_matching_requires}surface")
                single_token: Tag = Tag.from_name(f"{f_vocab_matching_requires}single-token")
                compound: Tag = Tag.from_name(f"{f_vocab_matching_requires}compound")

            class Forbids(Slots):
                masu_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}masu_stem")
                godan: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan")
                ichidan: Tag = Tag.from_name(f"{f_vocab_matching_forbids}ichidan")
                irrealis: Tag = Tag.from_name(f"{f_vocab_matching_forbids}irrealis")
                preceding_adverb: Tag = Tag.from_name(f"{f_vocab_matching_forbids}preceding_adverb")
                past_tense_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}past-tense-stem")
                dictionary_form_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}dictionary_form_stem")
                dictionary_form_prefix: Tag = Tag.from_name(f"{f_vocab_matching_forbids}dictionary_form_prefix")
                ichidan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_forbids}ichidan_imperative")
                godan_potential: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_potential")
                godan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_imperative")
                godan_imperative_prefix: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_imperative_prefix")
                te_form_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}te-form-stem")
                te_form_prefix: Tag = Tag.from_name(f"{f_vocab_matching_forbids}te-form-prefix")
                sentence_end: Tag = Tag.from_name(f"{f_vocab_matching_forbids}sentence-end")
                sentence_start: Tag = Tag.from_name(f"{f_vocab_matching_forbids}sentence-start")
                surface: Tag = Tag.from_name(f"{f_vocab_matching_forbids}surface")
                auto_yielding: Tag = Tag.from_name(f"{f_vocab_matching_forbids}auto_yielding")

            class Todo(Slots):
                with_preceding_vowel: Tag = Tag.from_name(f"{f_vocab_matching_todo}match-with-preceding-vowel")

            class Uses(Slots):
                prefix_is_not: Tag = Tag.from_name(f"{f_vocab_matching_uses}prefix-is-not")
                suffix_is_not: Tag = Tag.from_name(f"{f_vocab_matching_uses}suffix-is-not")
                required_prefix: Tag = Tag.from_name(f"{f_vocab_matching_uses}required-prefix")
                surface_is_not: Tag = Tag.from_name(f"{f_vocab_matching_uses}surface-is-not")

    priority_folder: str = f"{f_root}priority::"  # Keep as string for startswith() checks

    class Source(Slots):
        folder: str = f_source  # Keep as string for startswith() checks
        immersion_kit: Tag = Tag.from_name(f"{f_source}immersion_kit")
        jamdict: Tag = Tag.from_name(f"{f_source}jamdict")

    DisableKanaOnly: Tag = Tag.from_name("_disable_uk")
    UsuallyKanaOnly: Tag = Tag.from_name("_uk")
    TTSAudio: Tag = Tag.from_name("_tts_audio")
