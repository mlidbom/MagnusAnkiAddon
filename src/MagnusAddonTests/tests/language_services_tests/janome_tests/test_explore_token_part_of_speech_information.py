from __future__ import annotations

import pytest
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.inflection_types import InflectionTypes
from language_services.janome_ex.tokenizing.jn_parts_of_speech import POS
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer: JNTokenizer

# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = JNTokenizer()

@pytest.mark.parametrize("sentence, expected_tokens", [
    ("こんなに", [JNToken(POS.Adverb.particle_connection, "こんなに", "こんなに")]),
    ("こんなに疲れている", [
        JNToken(POS.Adverb.particle_connection, "こんなに", "こんなに"),
        JNToken(POS.Verb.independent, "疲れる", "疲れ", InflectionTypes.Ichidan.regular, InflectionForms.Continuative.renyōkei_masu_stem),
        JNToken(POS.Particle.conjunctive, "て", "て"),
        JNToken(POS.Verb.dependent, "いる", "いる", InflectionTypes.Ichidan.regular, InflectionForms.Basic.dictionary_form)]),
    ("こんなに食べている", [
        JNToken(POS.Adverb.particle_connection, "こんなに", "こんなに"),
        JNToken(POS.Verb.independent, "食べる", "食べ", InflectionTypes.Ichidan.regular, InflectionForms.Continuative.renyōkei_masu_stem),
        JNToken(POS.Particle.conjunctive, "て", "て"),
        JNToken(POS.Verb.dependent, "いる", "いる", InflectionTypes.Ichidan.regular, InflectionForms.Basic.dictionary_form)]),
    ("こんなにする", [
        JNToken(POS.pre_noun_adjectival, "こんな", "こんな"),
        JNToken(POS.Particle.CaseMarking.general, "に", "に"),
        JNToken(POS.Verb.independent, "する", "する", InflectionTypes.Sahen.suru, InflectionForms.Basic.dictionary_form)]),
    ("こんなに食べる", [
        JNToken(POS.pre_noun_adjectival, "こんな", "こんな"),
        JNToken(POS.Particle.CaseMarking.general, "に", "に"),
        JNToken(POS.Verb.independent, "食べる", "食べる", InflectionTypes.Ichidan.regular, InflectionForms.Basic.dictionary_form)]),
    ("そんなに好きだ", [
        JNToken(POS.Adverb.general, "そんなに", "そんなに"),
        JNToken(POS.Noun.na_adjective_stem, "好き", "好き"),
        JNToken(POS.bound_auxiliary, "だ", "だ", InflectionTypes.Special.da, InflectionForms.Basic.dictionary_form)]),
    ("そんなに走った", [
        JNToken(POS.Adverb.general, "そんなに", "そんなに"),
        JNToken(POS.Verb.independent, "走る", "走っ", InflectionTypes.Godan.ru_ending, InflectionForms.Continuative.ta_connection),
        JNToken(POS.bound_auxiliary, "た", "た", InflectionTypes.Special.ta, InflectionForms.Basic.dictionary_form)]),
    ("来い", [JNToken(POS.Verb.independent, "来る", "来い", InflectionTypes.Kahen.kuru_kanji, InflectionForms.ImperativeMeireikei.i)]),
    ("飛べない", [
        JNToken(POS.Verb.independent, "飛べる", "飛べ", InflectionTypes.Ichidan.regular, InflectionForms.Irrealis.general_irrealis_mizenkei),
        JNToken(POS.bound_auxiliary, "ない", "ない", InflectionTypes.Special.nai, InflectionForms.Basic.dictionary_form)
    ]),
    ("飛ばない", [
        JNToken(POS.Verb.independent, "飛ぶ", "飛ば", InflectionTypes.Godan.bu_ending, InflectionForms.Irrealis.general_irrealis_mizenkei),
        JNToken(POS.bound_auxiliary, "ない", "ない", InflectionTypes.Special.nai, InflectionForms.Basic.dictionary_form)
    ]),
    ("飛べ", [JNToken(POS.Verb.independent, "飛べる", "飛べ", InflectionTypes.Ichidan.regular, InflectionForms.Continuative.renyōkei_masu_stem)]),
])
def test_identify_something_words(sentence: str, expected_tokens: list[JNTokenizer]) -> None:
    tokenized = _tokenizer.tokenize(sentence)

    assert tokenized.tokens == expected_tokens
