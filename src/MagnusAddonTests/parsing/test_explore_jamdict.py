import pytest
from jamdict import Jamdict
from parsing.textparser import DictLookup
from unittest.mock import MagicMock
from note.wanivocabnote import WaniVocabNote

jam = Jamdict(memory_mode=True)
#jam = Jamdict(memory_mode=True) #Runs much faster after the first query that may take a minute!

def test_something() -> None:
    #print(jam.lookup("下さい"))
    #print(jam.lookup("くださる"))
    lookup = DictLookup.lookup_word_deep("ましょう")
    print(lookup)

@pytest.mark.parametrize('word, readings', [
    ("為る", ["する"]),
    ("為る", ["なる"])
])
def test_uk(word: str, readings: list[str]) -> None:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_vocab.return_value = word
    mock_instance.get_readings.return_value = readings

    dict_entry = DictLookup.lookup_vocab_word_shallow(mock_instance)
    assert dict_entry.is_kana_only() is True

@pytest.mark.parametrize('word, readings', [
    ("毎月", ["まいつき","まいげつ"])
])
def test_multi_readings(word: str, readings: list[str]) -> None:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_vocab.return_value = word
    mock_instance.get_readings.return_value = readings

    dict_entry = DictLookup.lookup_vocab_word_shallow(mock_instance)
    assert dict_entry is not None

@pytest.mark.parametrize('word, readings', [
    ("正す", ["ただす"]),
    ("角", ["かく","かど"])
])
def test_multi_matches(word: str, readings: list[str]) -> None:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_vocab.return_value = word
    mock_instance.get_readings.return_value = readings

    dict_entry = DictLookup.lookup_vocab_word_shallow(mock_instance)
    assert dict_entry is not None

@pytest.mark.parametrize('word, readings', [
    ("想像する", "そうぞうする"),
    ("に", ["に"]),
    ("しか", ["しか"])
])
def test_missing(word: str, readings: list[str]) -> None:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_vocab.return_value = word
    mock_instance.get_readings.return_value = readings

    dict_entry = DictLookup.lookup_vocab_word_shallow(mock_instance)
    assert dict_entry is not None

