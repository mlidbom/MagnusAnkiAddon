import pytest

from sysutils import kana_utils

@pytest.mark.parametrize("word, conjugation_bases, is_ichidan", [
    #irregular verbs
    ("くる", ['くれ', 'き', 'こ'], False),
    ("する", ['すれ', 'し', 'さ'], False),
    ('しようとする', ['しようとすれ', 'しようとし', 'しようとさ'], False),
    ("おいてくる", ['おいてくれ', 'おいてき', 'おいてこ'], False),

    #adjectives
    ("美味しい", ['美味しく'], False),

    #godan verbs
    ("走る", ["走り","走ら", "走れ"], False),
    ("使う", ["使い","使わ", "使え"], False),
    ("書く", ["書き","書か", "書け"], False),
    ("立つ", ["立ち","立た", "立て"], False),
    ("死ぬ", ["死に","死な", "死ね"], False),
    ("飛ぶ", ["飛び","飛ば", "飛べ"], False),
    ("読む", ["読み","読ま", "読め"], False),
    ("帰る", ["帰り","帰ら", "帰れ"], False),
    #ichidan verbs
    ("食べる", ["食べ"], True)
])
def test_identify_words(word: str, conjugation_bases: list[str], is_ichidan: bool) -> None:
    result = kana_utils.get_highlighting_conjugation_bases(word, is_ichidan)
    assert result == conjugation_bases