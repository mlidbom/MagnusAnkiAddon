import pytest
from note.wanivocabnote import WaniVocabNote
from parsing.jamdict_extensions.dict_entry import DictEntry
from parsing.jamdict_extensions.dict_lookup import DictLookup
from unittest.mock import MagicMock

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
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.is_uk()
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("毎月", ["まいつき","まいげつ"])
])
def test_multi_readings(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("元", ["もと"]),
    ("角", ["かく","かど"]),
    ("これ", ["これ"]),
    ("正す", ["ただす"]),
    ("て", ["て"])
])
def test_multi_matches(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() > 1

@pytest.mark.parametrize('word, readings', [
    ("に", ["に"]),
    ("しか", ["しか"]),
    ("ローマ字", ["ろーまじ"]),
    ("狩り", ["かり"])
])
def test_missing(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings', [
    ("田代島", ["たしろじま"])
])
def test_names(word: str, readings: list[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1

@pytest.mark.parametrize('word, readings, forms', [
    ("怪我", ["けが"], {"怪我", "ケガ", "けが"}),
    ("部屋", ["へや"], {"部屋"})
])
def test_valid_forms(word: str, readings:list[str], forms: set[str]) -> None:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1
    assert dict_entry.valid_forms() == forms


@pytest.mark.parametrize('word, readings, answer', [
    ("張り切る", ["はりきる"], "to? be-in-high-spirits/be-full-of-vigor-(vigour)/be-enthusiastic/be-eager/stretch-to-breaking-point"),
    ("部屋", ["へや"], "room/chamber | apartment/flat/pad | stable"),
    ("付く", ["つく"], "to? be-attached/be-connected-with/adhere/stick/cling | remain-imprinted/scar/stain/dye | bear-(fruit,-interest,-etc.) | be-acquired-(of-a-habit,-ability,-etc.)/increase-(of-strength,-etc.) | take-root | accompany/attend/follow/study-with | side-with/belong-to | possess/haunt | lit/lighted | settled/resolved/decided | given-(of-a-name,-price,-etc.) | sensed/perceived | lucky | become-(a-state,-condition,-etc.)")
])
def test_generate_answer(word: str, readings:list[str], answer: str) -> None:
    dict_entry = get_single_dict_entry(word, readings)
    generated_answer = dict_entry.generate_answer()
    print(generated_answer)
    assert generated_answer == answer


def get_single_dict_entry(word, readings) -> DictEntry:
    dict_entry = get_dict_entry(word, readings)
    assert dict_entry.found_words_count() == 1
    return dict_entry.entries[0]

def get_dict_entry(word, readings) -> DictLookup:
    mock_vocab = vocab_mock(word, readings)
    dict_entry = DictLookup.try_lookup_vocab_word_or_name(mock_vocab)
    return dict_entry

def vocab_mock(word: str, readings: list[str]) -> WaniVocabNote:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_question.return_value = word
    mock_instance.get_readings.return_value = readings
    return mock_instance

