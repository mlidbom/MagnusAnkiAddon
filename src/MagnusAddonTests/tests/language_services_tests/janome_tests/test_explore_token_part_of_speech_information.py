from __future__ import annotations

import pytest
from language_services.janome_ex.tokenizing.inflection_forms import InflectionForms
from language_services.janome_ex.tokenizing.inflection_types import InflectionTypes
from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPOS
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer: JNTokenizer

# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = JNTokenizer()

@pytest.mark.parametrize("sentence, expected_tokens", [
    ("こんなに", [JNToken(JNPOS.Adverb.particle_connection, "こんなに", "こんなに")]),
    ("こんなに疲れている", [
        JNToken(JNPOS.Adverb.particle_connection, "こんなに", "こんなに"),
        JNToken(JNPOS.Verb.independent, "疲れる", "疲れ", InflectionTypes.Ichidan.regular, InflectionForms.Continuative.renyoukei_masu_stem),
        JNToken(JNPOS.Particle.conjunctive, "て", "て"),
        JNToken(JNPOS.Verb.dependent, "いる", "いる", InflectionTypes.Ichidan.regular, InflectionForms.Basic.dictionary_form)]),
    ("こんなに食べている", [
        JNToken(JNPOS.Adverb.particle_connection, "こんなに", "こんなに"),
        JNToken(JNPOS.Verb.independent, "食べる", "食べ", InflectionTypes.Ichidan.regular, InflectionForms.Continuative.renyoukei_masu_stem),
        JNToken(JNPOS.Particle.conjunctive, "て", "て"),
        JNToken(JNPOS.Verb.dependent, "いる", "いる", InflectionTypes.Ichidan.regular, InflectionForms.Basic.dictionary_form)]),
    ("こんなにする", [
        JNToken(JNPOS.pre_noun_adjectival, "こんな", "こんな"),
        JNToken(JNPOS.Particle.CaseMarking.general, "に", "に"),
        JNToken(JNPOS.Verb.independent, "する", "する", InflectionTypes.Sahen.suru, InflectionForms.Basic.dictionary_form)]),
    ("こんなに食べる", [
        JNToken(JNPOS.pre_noun_adjectival, "こんな", "こんな"),
        JNToken(JNPOS.Particle.CaseMarking.general, "に", "に"),
        JNToken(JNPOS.Verb.independent, "食べる", "食べる", InflectionTypes.Ichidan.regular, InflectionForms.Basic.dictionary_form)]),
    ("そんなに好きだ", [
        JNToken(JNPOS.Adverb.general, "そんなに", "そんなに"),
        JNToken(JNPOS.Noun.na_adjective_stem, "好き", "好き"),
        JNToken(JNPOS.bound_auxiliary, "だ", "だ", InflectionTypes.Special.da, InflectionForms.Basic.dictionary_form)]),
    ("そんなに走った", [
        JNToken(JNPOS.Adverb.general, "そんなに", "そんなに"),
        JNToken(JNPOS.Verb.independent, "走る", "走っ", InflectionTypes.Godan.ru, InflectionForms.Continuative.ta_connection),
        JNToken(JNPOS.bound_auxiliary, "た", "た", InflectionTypes.Special.ta, InflectionForms.Basic.dictionary_form)]),
    ("来い", [JNToken(JNPOS.Verb.independent, "来る", "来い", InflectionTypes.Kahen.kuru_kanji, InflectionForms.ImperativeMeireikei.i)]),
    ("飛べない", [
        JNToken(JNPOS.Verb.independent, "飛べる", "飛べ", InflectionTypes.Ichidan.regular, InflectionForms.Irrealis.general_irrealis_mizenkei),
        JNToken(JNPOS.bound_auxiliary, "ない", "ない", InflectionTypes.Special.nai, InflectionForms.Basic.dictionary_form)
    ]),
    ("飛ばない", [
        JNToken(JNPOS.Verb.independent, "飛ぶ", "飛ば", InflectionTypes.Godan.bu, InflectionForms.Irrealis.general_irrealis_mizenkei),
        JNToken(JNPOS.bound_auxiliary, "ない", "ない", InflectionTypes.Special.nai, InflectionForms.Basic.dictionary_form)
    ]),
    ("飛べ", [JNToken(JNPOS.Verb.independent, "飛べる", "飛べ", InflectionTypes.Ichidan.regular, InflectionForms.Continuative.renyoukei_masu_stem)]),
    ("会う", [JNToken(JNPOS.Verb.independent, "会う", "会う", InflectionTypes.Godan.u_gemination, InflectionForms.Basic.dictionary_form)]),
])
def test_identify_something_words(sentence: str, expected_tokens: list[JNTokenizer]) -> None:
    tokenized = _tokenizer.tokenize(sentence)

    assert tokenized.tokens == expected_tokens
