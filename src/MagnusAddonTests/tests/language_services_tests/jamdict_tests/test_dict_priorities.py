from unittest.mock import MagicMock

import pytest

from language_services.jamdict_ex.dict_lookup import DictLookup
from note.vocabnote import VocabNote

@pytest.mark.parametrize('word, readings', [ # JPDB, CC100
    ("これ", ["これ"]),              # 40, 144
    ("震える", ["ふるえる"]),         # 701, 7716
    ("元", ["もと"]),               # 501, 560
    ("角", ["かく","かど"]),         # 2748, 6965
    ("正す", ["ただす"]),            # 7219, 9192
    ("震度", ["しんど"]),            # 40774, 8583 #todo
])
def test_priority_maximum(word: str, readings: list[str]) -> None: run_priority_test(word, readings, "priority_maximum")

@pytest.mark.parametrize('word, readings', [ # JPDB, CC100
    ("惨状", ["さんじょう"]),            # 9372, 22639
    ("優遇", ["ゆうぐう"]),              # 15205, 7069
])
def test_priority_high(word: str, readings: list[str]) -> None: run_priority_test(word, readings, "priority_high")

@pytest.mark.parametrize('word, readings', [ # JPDB, CC100
    ("最優遇", ["さいゆうぐう"]),         # 183459, ?
    ("不可分", ["ふかぶん"]),            # 51871, 34255 #todo
    ("不人気", ["ふにんき"]),            # 35219, 28125 #todo
    ("株式市場", ["かぶしきしじょう"])     # 59089, 36225 #todo
])
def test_priority_high_fixme(word: str, readings: list[str]) -> None: run_priority_test(word, readings, "priority_high")

@pytest.mark.parametrize('word, readings', [ # JPDB, CC100
    ("感涙", ["かんるい"]),           # 28855, 40035
])
def test_priority_medium(word: str, readings: list[str]) -> None: run_priority_test(word, readings, "priority_medium")

@pytest.mark.parametrize('word, readings', [ # JPDB, CC100
    ("力不足", ["ちからぶそく"]),      # 13298, 35619 #todo
    ("号室", ["ごうしつ"])
])
def test_priority_low(word: str, readings: list[str]) -> None: run_priority_test(word, readings, "priority_low")

def run_priority_test(word: str, readings: list[str], expected:str) -> None:
    dict_entry = get_dict_entry(word, readings)
    spec = dict_entry.priority_spec()
    assert spec.priority_string == expected

def get_dict_entry(word: str, readings: list[str]) -> DictLookup:
    mock_vocab = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_vocab)
    return dict_entry

def vocab_mock(word: str, readings: list[str]) -> VocabNote:
    mock_instance = MagicMock(spec=VocabNote)
    mock_instance.get_question.return_value = word
    mock_instance.get_readings.return_value = readings
    return mock_instance

