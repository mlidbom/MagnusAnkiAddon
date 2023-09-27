import pytest

from parsing.janome_extensions.parts_of_speech import POS
from parsing.janome_extensions.token_ext import TokenExt
from parsing.janome_extensions.tokenizer_ext import TokenizerExt

_tokenizer:TokenizerExt

@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = TokenizerExt()

@pytest.mark.parametrize('sentence, expected_tokens', [
    ("こんなに", [TokenExt(POS.Adverb.particle_connection, "こんなに", "こんなに")]),
    ("こんなに疲れている", [
        TokenExt(POS.Adverb.particle_connection, "こんなに", "こんなに"),
        TokenExt(POS.Verb.independent,           "疲れる",   "疲れ", "一段", "連用形"),
        TokenExt(POS.Particle.conjunctive,       "て",      "て"),
        TokenExt(POS.Verb.dependent, "いる", "いる", "一段", "基本形")]),
    ("こんなに食べている", [
        TokenExt(POS.Adverb.particle_connection, "こんなに", "こんなに"),
        TokenExt(POS.Verb.independent,           "食べる",   "食べ", "一段", "連用形"),
        TokenExt(POS.Particle.conjunctive,       "て",      "て"),
        TokenExt(POS.Verb.dependent, "いる", "いる", "一段", "基本形")]),
    ("こんなにする",      [
        TokenExt(POS.pre_noun_adjectival,          "こんな", "こんな"),
        TokenExt(POS.Particle.CaseMarking.general, "に",    "に"),
        TokenExt(POS.Verb.independent,             "する",  "する", "サ変・スル", "基本形")]),
    ("こんなに食べる", [
        TokenExt(POS.pre_noun_adjectival,          "こんな", "こんな"),
        TokenExt(POS.Particle.CaseMarking.general, "に",    "に"),
        TokenExt(POS.Verb.independent,             "食べる", "食べる", "一段", "基本形")]),
    ("そんなに好きだ",    [
        TokenExt(POS.Adverb.general,               "そんなに", "そんなに"),
        TokenExt(POS.Noun.na_adjective_stem,       "好き",    "好き"),
        TokenExt(POS.bound_auxiliary,              "だ",      "だ", "特殊・ダ", "基本形")]),
    ("そんなに走った",    [
        TokenExt(POS.Adverb.general,   "そんなに", "そんなに"),
        TokenExt(POS.Verb.independent, "走る",    "走っ",     "五段・ラ行", "連用タ接続"),
        TokenExt(POS.bound_auxiliary,  "た",      "た",      "特殊・タ",   "基本形")])
])
def test_identify_something_words(sentence: str, expected_tokens: list[TokenizerExt]) -> None:
    tokenized = _tokenizer.tokenize(sentence)

    assert expected_tokens == tokenized.tokens
