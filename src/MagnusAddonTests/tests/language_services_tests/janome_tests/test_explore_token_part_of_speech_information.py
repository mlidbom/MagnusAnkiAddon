from __future__ import annotations

import pytest
from language_services.janome_ex.tokenizing.jn_parts_of_speech import POS
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer

_tokenizer:JNTokenizer

# noinspection PyUnusedFunction
@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = JNTokenizer()

@pytest.mark.parametrize('sentence, expected_tokens', [
    ("こんなに", [JNToken(POS.Adverb.particle_connection, "こんなに", "こんなに")]),
    ("こんなに疲れている", [
        JNToken(POS.Adverb.particle_connection, "こんなに", "こんなに"),
        JNToken(POS.Verb.independent, "疲れる", "疲れ", "一段", "連用形"),
        JNToken(POS.Particle.conjunctive, "て", "て"),
        JNToken(POS.Verb.dependent, "いる", "いる", "一段", "基本形")]),
    ("こんなに食べている", [
        JNToken(POS.Adverb.particle_connection, "こんなに", "こんなに"),
        JNToken(POS.Verb.independent, "食べる", "食べ", "一段", "連用形"),
        JNToken(POS.Particle.conjunctive, "て", "て"),
        JNToken(POS.Verb.dependent, "いる", "いる", "一段", "基本形")]),
    ("こんなにする",      [
        JNToken(POS.pre_noun_adjectival, "こんな", "こんな"),
        JNToken(POS.Particle.CaseMarking.general, "に", "に"),
        JNToken(POS.Verb.independent, "する", "する", "サ変・スル", "基本形")]),
    ("こんなに食べる", [
        JNToken(POS.pre_noun_adjectival, "こんな", "こんな"),
        JNToken(POS.Particle.CaseMarking.general, "に", "に"),
        JNToken(POS.Verb.independent, "食べる", "食べる", "一段", "基本形")]),
    ("そんなに好きだ",    [
        JNToken(POS.Adverb.general, "そんなに", "そんなに"),
        JNToken(POS.Noun.na_adjective_stem, "好き", "好き"),
        JNToken(POS.bound_auxiliary, "だ", "だ", "特殊・ダ", "基本形")]),
    ("そんなに走った",    [
        JNToken(POS.Adverb.general, "そんなに", "そんなに"),
        JNToken(POS.Verb.independent, "走る", "走っ", "五段・ラ行", "連用タ接続"),
        JNToken(POS.bound_auxiliary, "た", "た", "特殊・タ", "基本形")])
])
def test_identify_something_words(sentence: str, expected_tokens: list[JNTokenizer]) -> None:
    tokenized = _tokenizer.tokenize(sentence)

    assert expected_tokens == tokenized.tokens
