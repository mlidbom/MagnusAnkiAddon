import pytest

from sysutils import kana_utils

@pytest.mark.parametrize("word, conjugation_bases", [
    ("走る", ['走']),
    ("くる", ['き', 'こ']),
    ('しようとする', ['しようとし']),
    ("おいてくる", ['おいてき', 'おいてこ'])
])
def test_identify_words(word: str, conjugation_bases: list[str]) -> None:
    result = kana_utils.get_highlighting_conjugation_bases(word)
    assert result == conjugation_bases