from __future__ import annotations

import pytest
from jaspythonutils.sysutils import kana_utils


@pytest.mark.parametrize("kana,expected_romaji, expected_hiragana, expected_katakana", [
    ("かな", "kana", "かな", "カナ"),
    ("かく", "kaku", "かく", "カク"),
    ("かく はく", "kaku haku", "かく はく", "カク ハク"),
    ("ジャッツ", "jattsu", "じゃっつ", "ジャッツ"),
    ("じゃっつ", "jattsu", "じゃっつ", "ジャッツ"),
    ("ジャッ", "ja", "じゃ", "ジャ"),
    ("じゃっ", "ja", "じゃ", "ジャ"),
    ("キャク", "kyaku", "きゃく", "キャク"),
    ("チャ", "cha", "ちゃ", "チャ")
])
def test_romaji_kana_roundtripping(kana:str, expected_romaji:str, expected_hiragana:str, expected_katakana:str) -> None:
    romaji = kana_utils.romanize(kana)
    assert romaji == expected_romaji
    assert kana_utils.romaji_to_hiragana(romaji) == expected_hiragana
    assert kana_utils.romaji_to_katakana(romaji) == expected_katakana
