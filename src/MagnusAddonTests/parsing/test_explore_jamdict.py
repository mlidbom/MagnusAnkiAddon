import pytest
from note.wanivocabnote import WaniVocabNote
from parsing.jamdict_extensions.dict_lookup import DictLookup
from unittest.mock import MagicMock


def vocab_mock(word: str, readings: list[str]) -> WaniVocabNote:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_question.return_value = word
    mock_instance.get_readings.return_value = readings
    return mock_instance

#TODO: See if we can find a way to parse suru out of sentences such that the verbalizing suffix can be
# handled separately from the stand-alone word. The pos information from Janome might allow this
# @pytest.mark.parametrize('word, readings', [
#     ("する", ["する"])
# ])
# def test_separate_usages_verb_suffix(word: str, readings: list[str]) -> None:
#     mock_instance = vocab_mock(word, readings)
#     dict_entry = DictLookup.lookup_vocab_word_or_name(mock_instance)
#     assert dict_entry.is_uk()
#     assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("為る", ["する"]),
    ("為る", ["なる"])
])
def test_uk(word: str, readings: list[str]) -> None:
    mock_instance = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_instance)
    assert dict_entry.is_uk()
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("毎月", ["まいつき","まいげつ"])
])
def test_multi_readings(word: str, readings: list[str]) -> None:
    mock_instance = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_instance)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("元", ["もと"]),
    ("角", ["かく","かど"]),
    ("これ", ["これ"]),
    ("正す", ["ただす"]),
    ("て", ["て"])
])
def test_multi_matches(word: str, readings: list[str]) -> None:
    mock_instance = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_instance)
    assert dict_entry.found_words_count() > 1

@pytest.mark.parametrize('word, readings', [
    ("に", ["に"]),
    ("しか", ["しか"]),
    ("ローマ字", ["ろーまじ"]),
    ("狩り", ["かり"])
])
def test_missing(word: str, readings: list[str]) -> None:
    mock_instance = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_instance)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("田代島", ["たしろじま"])
])
def test_names(word: str, readings: list[str]) -> None:
    mock_instance = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_instance)
    assert dict_entry.found_words_count() == 1


