from __future__ import annotations

from jastudio.language_services import  conjugator
import pytest


@pytest.mark.parametrize("word, conjugation_bases", [
    # irregular verbs
    ("くる", ["き", "こ", "くれ", "き"]),
    ("する", ["し", "さ", "すれ", "し", "せ"]),
    ("いく", ["いき", "いか", "いけ", "いっ", "いこ"]),
    ("行く", ["行き", "行か", "行け", "行っ", "行こ"]),
    ("います", ["いまし", "いませ"]),
    ("しようとする", ["しようとし", "しようとさ", "しようとすれ", "しようとし", "しようとせ"]),
    ("おいてくる", ["おいてき", "おいてこ", "おいてくれ", "おいてき"]),
])
def test_irregular_verbs(word: str, conjugation_bases: list[str]) -> None:
    run_tests(word, conjugation_bases)

@pytest.mark.parametrize("word, conjugation_bases, is_ichidan", [
    ("食べる", ["食べり", "食べら", "食べれ", "食べっ", "食べ", "食べろ", "食べな"], False),
    ("食べる", ["食べ", "食べろ", "食べな"], True),
])
def test_ichidan(word: str, conjugation_bases: list[str], is_ichidan: bool) -> None:
    run_tests(word, conjugation_bases, is_ichidan)

@pytest.mark.parametrize("word, conjugation_bases", [
    # adjectives
    ("美味しい", ["美味しく", "美味しけ", "美味しか"]),

    # irregular adjective
    ("いい", ["よく", "よけ", "よか", "よかっ"]),
])
def test_adjectives(word: str, conjugation_bases: list[str]) -> None:
    run_tests(word, conjugation_bases)

@pytest.mark.parametrize("word, conjugation_bases", [
    # aru verbs
    ("なさる", ["なさい", "なさら", "なされ", "なさっ"]),
    ("くださる", ["ください", "くださら", "くだされ", "くださっ"]),
    ("いらっしゃる", ["いらっしゃい", "いらっしゃら", "いらっしれば", "いらっしゃっ"]),
    ("おっしゃる", ["おっしゃい", "おっしゃら", "おっしれば", "おっしゃっ"]),
    ("ござる", ["ござい", "ござら", "ござれ", "ござっ"])
])
def test_aru_verbs(word: str, conjugation_bases: list[str]) -> None:
    run_tests(word, conjugation_bases)

@pytest.mark.parametrize("word, conjugation_bases", [
    # unknown godan verbs should add the ichidan endings
    ("走る", ["走り", "走ら", "走れ", "走っ", "走", "走ろ", "走な"]),
    ("帰る", ["帰り", "帰ら", "帰れ", "帰っ", "帰", "帰ろ", "帰な"]),

    #ordinary godan
    ("使う", ["使い", "使わ", "使え", "使っ"]),
    ("書く", ["書き", "書か", "書け", "書い"]),
    ("立つ", ["立ち", "立た", "立て", "立っ"]),
    ("死ぬ", ["死に", "死な", "死ね", "死ん"]),
    ("飛ぶ", ["飛び", "飛ば", "飛べ", "飛ん"]),
    ("読む", ["読み", "読ま", "読め", "読ん"]),
])
def test_unknown_godan(word: str, conjugation_bases: list[str]) -> None:
    run_tests(word, conjugation_bases)

@pytest.mark.parametrize("word, conjugation_bases", [
    # godan verbs
    ("走る", ["走り", "走ら", "走れ", "走っ"]),
    ("帰る", ["帰り", "帰ら", "帰れ", "帰っ"]),
    ("使う", ["使い", "使わ", "使え", "使っ"]),
    ("書く", ["書き", "書か", "書け", "書い"]),
    ("立つ", ["立ち", "立た", "立て", "立っ"]),
    ("死ぬ", ["死に", "死な", "死ね", "死ん"]),
    ("飛ぶ", ["飛び", "飛ば", "飛べ", "飛ん"]),
    ("読む", ["読み", "読ま", "読め", "読ん"]),
])
def test_known_godan(word: str, conjugation_bases: list[str]) -> None:
    run_tests(word, conjugation_bases, is_godan=True)

def run_tests(word: str, conjugation_bases: list[str], is_ichidan: bool = False, is_godan: bool = False) -> None:
    result = conjugator.get_word_stems(word, is_ichidan, is_godan)
    assert result == conjugation_bases
    if len(conjugation_bases) > 1:
        i_stem = conjugator.get_i_stem(word, is_ichidan, is_godan)
        assert i_stem == conjugation_bases[0]

    if is_ichidan:
        return

    if len(conjugation_bases) > 2:
        a_stem = conjugator.get_a_stem(word, is_ichidan, is_godan)
        assert a_stem == conjugation_bases[1]
    if len(conjugation_bases) > 3:
        e_stem = conjugator.get_e_stem(word, is_ichidan, is_godan)
        assert e_stem == conjugation_bases[2]
    if len(conjugation_bases) > 4:
        te_stem = conjugator.get_te_stem(word, is_ichidan, is_godan)
        assert te_stem == conjugation_bases[3]
