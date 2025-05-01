import pytest

import language_services.conjugator

@pytest.mark.parametrize("word, conjugation_bases, is_ichidan, is_godan", [
    # irregular verbs
    ("くる", ['き', 'こ', 'くれ', 'き'], False, False),
    ("する", ['し', 'さ', 'すれ', 'し'], False, False),
    ("いく", ['いき', 'いか', 'いけ', 'いっ', 'いこ'], False, False),
    ("行く", ['行き', '行か', '行け', '行っ', '行こ'], False, False),
    ("います", ['いまし', 'いませ'], False, False),
    ('しようとする', ['しようとし', 'しようとさ', 'しようとすれ', 'しようとし'], False, False),
    ("おいてくる", ['おいてき', 'おいてこ', 'おいてくれ', 'おいてき'], False, False),

    # adjectives
    ("美味しい", ['美味しく', '美味しけ', '美味しか'], False, False),

    # irregular adjective
    ("いい", ['よく', 'よけ', 'よか'], False, False),

    # godan verbs
    ("走る", ["走り", "走ら", "走れ", "走っ", "走"], False, False),
    ("帰る", ["帰り", "帰ら", "帰れ", "帰っ", "帰"], False, False),
    ("走る", ["走り", "走ら", "走れ", "走っ"], False, True),
    ("帰る", ["帰り", "帰ら", "帰れ", "帰っ"], False, True),
    ("使う", ["使い", "使わ", "使え", "使っ"], False, False),
    ("書く", ["書き", "書か", "書け", "書い"], False, False),
    ("立つ", ["立ち", "立た", "立て", "立っ"], False, False),
    ("死ぬ", ["死に", "死な", "死ね", "死ん"], False, False),
    ("飛ぶ", ["飛び", "飛ば", "飛べ", "飛ん"], False, False),
    ("読む", ["読み", "読ま", "読め", "読ん"], False, False),

    # ichidan verbs
    ("食べる", ['食べり', '食べら', '食べれ', '食べっ', '食べ'], False, False),
    ("食べる", ["食べ"], True, False),

    # aru verbs
    ('なさる', ['なさい', 'なさら', 'なされ', 'なさっ'], False, False),
    ('くださる', ['ください', 'くださら', 'くだされ', 'くださっ'], False, False),
    ('いらっしゃる', ['いらっしゃい', 'いらっしゃら', 'いらっしれば', 'いらっしゃっ'], False, False),
    ('おっしゃる', ['おっしゃい', 'おっしゃら', 'おっしれば', 'おっしゃっ'], False, False),
    ('ござる', ['ござい', 'ござら', 'ござれ', 'ござっ'], False, False)
])
def test_identify_stems(word: str, conjugation_bases: list[str], is_ichidan: bool, is_godan: bool) -> None:
    result = language_services.conjugator.get_word_stems(word, is_ichidan, is_godan)
    assert result == conjugation_bases

    if len(conjugation_bases) > 1:
        i_stem = language_services.conjugator.get_i_stem(word, is_ichidan, is_godan)
        assert i_stem == conjugation_bases[0]
    if len(conjugation_bases) > 2:
        a_stem = language_services.conjugator.get_a_stem(word, is_ichidan, is_godan)
        assert a_stem == conjugation_bases[1]
    if len(conjugation_bases) > 3:
        e_stem = language_services.conjugator.get_e_stem(word, is_ichidan, is_godan)
        assert e_stem == conjugation_bases[2]
    if len(conjugation_bases) > 4:
        te_stem = language_services.conjugator.get_te_stem(word, is_ichidan, is_godan)
        assert te_stem == conjugation_bases[3]
