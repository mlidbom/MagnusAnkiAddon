import pytest

from sysutils import kana_utils

@pytest.mark.parametrize("text,expected", [
    ("かな", "kana"),
    ("かく", "kaku"),
    ("かく はく", "kaku haku"),
    ("ジャッツ", "jattsu"),
    ("じゃっつ", "jattsu"),
    ("ジャッ", "ja"),
    ("じゃっ", "ja"),
    ("キャク", "kyaku"),
    ("チャ", "cha")
])
def test_romanization(text: str, expected: str) -> None:
    assert kana_utils.romanize(text) == expected
