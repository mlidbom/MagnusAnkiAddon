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

def test_uk() -> None:
    mock_instance = MagicMock(spec=WaniVocabNote)
    mock_instance.get_vocab.return_value = "為る"
    mock_instance.get_reading.return_value = "する"

    dict_entry = DictLookup.lookup_vocab_word_shallow(mock_instance)
    assert dict_entry.is_kana_only() is True

def test_pos() -> None:
    for pos in jam.all_pos():
        print(pos)  # pos is a string

def test_name() -> None:
    for ne_type in jam.all_ne_type():
        print(ne_type)  # ne_type is a string

