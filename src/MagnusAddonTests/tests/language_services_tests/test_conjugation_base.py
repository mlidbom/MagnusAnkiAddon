import pytest

from sysutils import kana_utils

@pytest.mark.parametrize('word, conjugation_base', [
    ("走る", '走'),
    ('しようとする', 'しようとし')
])
def test_identify_words(word: str, conjugation_base: str) -> None:
    result = kana_utils.get_conjugation_base(word)
    assert result == conjugation_base