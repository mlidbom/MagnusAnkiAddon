import pytest

from sysutils import kana_utils

@pytest.mark.parametrize("text,expected", [
    ("かな", "kana"),
    ("かく", "kaku"),
    ("かく はく", "kaku haku")
])
def test_romanization(text: str, expected: str) -> None:
    assert expected == kana_utils.romanize(text)
