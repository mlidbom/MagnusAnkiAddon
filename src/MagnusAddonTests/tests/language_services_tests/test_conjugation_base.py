import pytest

from sysutils import kana_utils

@pytest.mark.parametrize("word, conjugation_bases, is_ichidan", [
    #irregular verbs
    ("くる", ['くれ', 'き', 'こ'], False),
    ("する", ['すれ', 'し', 'さ'], False),
    ('しようとする', ['しようとすれ', 'しようとし', 'しようとさ'], False),
    ("おいてくる", ['おいてくれ', 'おいてき', 'おいてこ'], False),

    #adjectives
    ("美味しい", ['美味しく', '美味し'], False),

    #godan verbs
    ("走る", ["走り","走ら", "走れ", "走"], False),
    ("使う", ["使い","使わ", "使え", "使"], False),
    ("書く", ["書き","書か", "書け", "書"], False),
    ("立つ", ["立ち","立た", "立て", "立"], False),
    ("死ぬ", ["死に","死な", "死ね", "死"], False),
    ("飛ぶ", ["飛び","飛ば", "飛べ", "飛"], False),
    ("読む", ["読み","読ま", "読め", "読"], False),
    ("帰る", ["帰り","帰ら", "帰れ", "帰"], False),
    #ichidan verbs
    ("食べる", ["食べ"], True)
])
def test_identify_words(word: str, conjugation_bases: list[str], is_ichidan: bool) -> None:
    result = kana_utils.get_highlighting_conjugation_bases(word, is_ichidan)
    assert result == conjugation_bases