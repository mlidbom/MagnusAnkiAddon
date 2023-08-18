import pytest
from janome.tokenizer import Tokenizer

from parsing.janomeutils import extract_dictionary_forms
from parsing.textparser import ParsedWord, identify_first_word, identify_words2

_tokenizer = Tokenizer()

#TODO: See if we can't find a way to parse suru out of sentences such that the verbalizing suffix can be
# handled separately from the stand-alone word.
def test_suffix_suru_recognized_as_suffix() -> None:
    result = list(_tokenizer.tokenize("心配する"))
    print(result)
    assert result == "NOT HAPPENING"

def test_stand_alone_suru_recognized_as_stand_alone() -> None:
    result = list(_tokenizer.tokenize("する"))
    print(result)
    assert result == "NOT HAPPENING"

@pytest.mark.parametrize('sentence, expected_output', [
    ("走る",
     [ParsedWord('走る', '')]),
    ("走って",
     [ParsedWord('走る', ''),
      ParsedWord('て', '')]),
    ("これをください。",
     [ParsedWord('これ', ''),
      ParsedWord('を', ''),
      ParsedWord('くださる', ''),
      ParsedWord('ください', '')]),
    ("ハート形",
     [ParsedWord('ハート', ''),
      ParsedWord('ハート形', ''),
      ParsedWord('形', '')]),
    ("私が行きましょう。",
     [ParsedWord('私', ''),
      ParsedWord('が', ''),
      ParsedWord('行く', ''),
      ParsedWord('行き', ''),
      ParsedWord('ます', ''),
      ParsedWord('ましょ', ''),
      ParsedWord('ましょう', ''),
      ParsedWord('う', '')]),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     [ParsedWord('１', ''),
      ParsedWord('１人', ''),
      ParsedWord('１人で', ''),
      ParsedWord('人', ''),
      ParsedWord('で', ''),
      ParsedWord('いる', ''),
      ParsedWord('時間', ''),
      ParsedWord('が', ''),
      ParsedWord('これ', ''),
      ParsedWord('これほど', ''),
      ParsedWord('ほど', ''),
      ParsedWord('まで', ''),
      ParsedWord('までに', ''),
      ParsedWord('に', ''),
      ParsedWord('長い', ''),
      ParsedWord('感じる', ''),
      ParsedWord('と', ''),
      ParsedWord('とは', ''),
      ParsedWord('は', '')]),
])
def test_identify_words(sentence: str, expected_output: list[ParsedWord]) -> None:
    result = identify_words2(sentence)
    print(result)
    assert result == expected_output

def test_ignores_noise_characters() -> None:
    result = identify_words2(".,:;/|。、ー")
    print(result)
    assert result == [ParsedWord("ー","")]

@pytest.mark.parametrize('sentence, expected_output', [
    ("走る",
     [ParsedWord('走る', 'verb,independent,*,*')]),
    ("走って",
     [ParsedWord('走る', 'verb,independent,*,*'),
      ParsedWord('て', 'particle,conjunctive,*,*')]),
    ("これをください。",
     [ParsedWord('これ', 'noun,pronoun,general,*'),
      ParsedWord('を', 'particle,case-particle,general,*'),
      ParsedWord('くださる', 'verb,independent,*,*')]),  # BAD wrong word, correct word missing
    ("ハート形",
     [ParsedWord('ハート', 'noun,general,*,*'),
      ParsedWord('形', 'noun,suffix,general,*')]),
    ("私が行きましょう。",
     [ParsedWord('私', 'noun,pronoun,general,*'),
      ParsedWord('が', 'particle,case-particle,general,*'),
      ParsedWord('行く', 'verb,independent,*,*'),
      ParsedWord('ます', 'auxiliary-verb,*,*,*'),
      ParsedWord('う', 'auxiliary-verb,*,*,*')]),
    ("ハート形",
     [ParsedWord('ハート', 'noun,general,*,*'),
      ParsedWord('形', 'noun,suffix,general,*')]), #BAD compound word missing
    ("彼の日本語のレベルは私と同じ位だ。",
     [ParsedWord('彼', 'noun,pronoun,general,*'),
      ParsedWord('の', 'particle,adnominalization,*,*'),
      ParsedWord('日本語', 'noun,general,*,*'),
      ParsedWord('レベル', 'noun,general,*,*'),
      ParsedWord('は', 'particle,binding,*,*'),
      ParsedWord('私', 'noun,pronoun,general,*'),
      ParsedWord('と', 'particle,case-particle,general,*'),
      ParsedWord('同じ', 'adnominal-adjective,*,*,*'),
      ParsedWord('位', 'noun,adverbial,*,*'),
      ParsedWord('だ', 'auxiliary-verb,*,*,*')]
     )
])
def test_extract_dictionary_forms(sentence: str, expected_output: list[ParsedWord]) -> None:
    result = extract_dictionary_forms(sentence)
    print(result)
    assert result == expected_output


@pytest.mark.parametrize('sentence, expected_output', [
    ("ハート形", "ハート形"),
    ("走る", "走る"),
    ("走って", "走る"),
    ("走り回る", "走り回る"),
    ("走って", "走る")
])
def test_identify_word(sentence: str, expected_output: str) -> None:
    result = identify_first_word(sentence)
    assert result == expected_output
