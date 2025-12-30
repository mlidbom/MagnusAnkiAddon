from __future__ import annotations

from autoslot import Slots

f_root = "-::"
f_sentence: str = f"{f_root}sentence::"
f_kanji: str = f"{f_root}kanji::"
f_sentence_uses: str = f"{f_sentence}uses::"
f_vocab: str = f"{f_root}vocab::"
f_vocab_matching: str = f"{f_vocab}matching::"
f_vocab_matching_requires: str = f"{f_vocab_matching}requires::"
f_vocab_matching_forbids: str = f"{f_vocab_matching}forbids::"
f_vocab_matching_todo: str = f"{f_vocab_matching}todo::"
f_vocab_matching_uses: str = f"{f_vocab_matching}uses::"
f_source = "source::"
class Tags(Slots):
    class Sentence(Slots):
        class Uses(Slots):
            incorrect_matches: str = f"{f_sentence_uses}incorrect-matches"
            hidden_matches: str = f"{f_sentence_uses}hidden-matches"

    class Kanji(Slots):
        is_radical: str = f"{f_kanji}is-radical"
        is_radical_purely: str = f"{f_kanji}is-radical-purely"
        is_radical_silent: str = f"{f_kanji}is-radical-silent"
        in_vocab_main_form: str = f"{f_kanji}in-vocab-main-form"
        in_any_vocab_form: str = f"{f_kanji}in-any-vocab-form"

        with_single_kanji_vocab: str = f"{f_kanji}single-kanji-vocab"
        with_single_kanji_vocab_with_different_reading: str = f"{f_kanji}single-kanji-vocab-with-different-reading"
        with_studying_single_kanji_vocab_with_different_reading: str = f"{f_kanji}studying-single-kanji-vocab-with-different-reading"
        with_no_primary_on_readings: str = f"{f_kanji}no-primary-on-readings"
        with_no_primary_readings: str = f"{f_kanji}no-primary-readings"
        with_studying_vocab: str = f"{f_kanji}studying-vocab"
        with_vocab_with_primary_on_reading: str = f"{f_kanji}has-vocab-with-primary-on-reading"
        with_studying_vocab_with_primary_on_reading: str = f"{f_kanji}studying-vocab-with-primary-on-reading"

        has_studying_vocab_with_no_matching_primary_reading: str = f"{f_kanji}has-studying-vocab-with-no-matching-primary-reading"
        has_studying_vocab_for_each_primary_reading: str = f"{f_kanji}has-studying-vocab-for-each-primary-reading"
        has_primary_reading_with_no_studying_vocab: str = f"{f_kanji}has-primary-reading-with-no-studying-vocab"
        has_non_primary_on_reading_vocab: str = f"{f_kanji}has-non-primary-on-reading-vocab"
        has_non_primary_on_reading_vocab_with_only_known_kanji: str = f"{f_kanji}has-non-primary-on-reading-vocab-with-only-known-kanji"

    class Vocab(Slots):
        root: str = f_vocab
        has_no_studying_sentences: str = f"{f_vocab}has-no-studying-sentences"
        question_overrides_form: str = f"{f_vocab}question-overrides-form"

        class Matching(Slots):
            yield_last_token_to_overlapping_compound: str = f"{f_vocab_matching}yield-last-token-to-upcoming-compound"
            is_poison_word: str = f"{f_vocab_matching}is-poison-word"
            is_inflecting_word: str = f"{f_vocab_matching}is-inflecting-word"

            class Requires(Slots):
                a_stem: str = f"{f_vocab_matching_requires}a-stem"
                e_stem: str = f"{f_vocab_matching_requires}e-stem"
                past_tense_stem: str = f"{f_vocab_matching_requires}past-tense-stem"
                ichidan_imperative: str = f"{f_vocab_matching_requires}ichidan_imperative"
                godan_potential: str = f"{f_vocab_matching_requires}godan_potential"
                godan_imperative: str = f"{f_vocab_matching_requires}godan_imperative"
                godan_imperative_prefix: str = f"{f_vocab_matching_forbids}godan_imperative_prefix"
                te_form_stem: str = f"{f_vocab_matching_requires}te-form-stem"
                sentence_end: str = f"{f_vocab_matching_requires}sentence-end"
                sentence_start: str = f"{f_vocab_matching_requires}sentence-start"
                exact_match: str = f"{f_vocab_matching_requires}exact-match"
                single_token: str = f"{f_vocab_matching_requires}single-token"
                compound: str = f"{f_vocab_matching_requires}compound"

            class Forbids(Slots):
                a_stem: str = f"{f_vocab_matching_forbids}a-stem"
                e_stem: str = f"{f_vocab_matching_forbids}e-stem"
                past_tense_stem: str = f"{f_vocab_matching_forbids}past-tense-stem"
                ichidan_imperative: str = f"{f_vocab_matching_forbids}ichidan_imperative"
                godan_potential: str = f"{f_vocab_matching_forbids}godan_potential"
                godan_imperative: str = f"{f_vocab_matching_forbids}godan_imperative"
                godan_imperative_prefix: str = f"{f_vocab_matching_forbids}godan_imperative_prefix"
                te_form_stem: str = f"{f_vocab_matching_forbids}te-form-stem"
                sentence_end: str = f"{f_vocab_matching_forbids}sentence-end"
                sentence_start: str = f"{f_vocab_matching_forbids}sentence-start"
                exact_match: str = f"{f_vocab_matching_forbids}exact-match"
                auto_yielding: str = f"{f_vocab_matching_forbids}auto_yielding"

            class Todo(Slots):
                with_preceding_vowel: str = f"{f_vocab_matching_todo}match-with-preceding-vowel"

            class Uses(Slots):
                prefix_is_not: str = f"{f_vocab_matching_uses}prefix-is-not"
                suffix_is_not: str = f"{f_vocab_matching_uses}suffix-is-not"
                required_prefix: str = f"{f_vocab_matching_uses}required-prefix"
                surface_is_not: str = f"{f_vocab_matching_uses}surface-is-not"

    priority_folder: str = f"{f_root}priority::"

    class Source(Slots):
        folder: str = f_source
        immersion_kit: str = f"{f_source}immersion_kit"
        jamdict: str = f"{f_source}jamdict"

    DisableKanaOnly: str = "_disable_uk"
    UsuallyKanaOnly: str = "_uk"
    TTSAudio: str = "_tts_audio"
