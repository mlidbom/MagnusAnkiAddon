import pytest

from parsing.janomeutils import extract_dictionary_forms
from parsing.textparser import ParsedWord, identify_first_word, identify_words2


@pytest.mark.parametrize('sentence, expected_output', [
    ("走る", ["走る"]),
    ("走って", ["走る", "て"]),
    ("これをください。", ['これ', 'を', 'ください', 'くださる']),
    ("ハート形", ['ハート', 'ハート形', '形']),
    #("私が行きましょう。", ['私', 'が', '行く'])
])
def test_identify_words(sentence: str, expected_output: list[ParsedWord]) -> None:
    result = identify_words2(sentence)
    print(result)
    assert result == expected_output


@pytest.mark.parametrize('sentence, expected_output', [
    ("走る", [ParsedWord('走る', 'verb,independent,*,*')]),
    ("走って",
     [ParsedWord('走る', 'verb,independent,*,*'),
      ParsedWord('て', 'particle,conjunctive,*,*')]),
    ("これをください。",
     [ParsedWord('これ', 'noun,pronoun,general,*'),
      ParsedWord('を', 'particle,case-particle,general,*'),
      ParsedWord('くださる', 'verb,independent,*,*')]),  # BAD
    ("ハート形",
     [ParsedWord('ハート', 'noun,general,*,*'),
      ParsedWord('形', 'noun,suffix,general,*')]),
    ("私が行きましょう。",
     [ParsedWord('私', 'noun,pronoun,general,*'),
      ParsedWord('が', 'particle,case-particle,general,*'),
      ParsedWord('行く', 'verb,independent,*,*'),
      ParsedWord('ます', 'auxiliary-verb,*,*,*'),
      ParsedWord('う', 'auxiliary-verb,*,*,*')])
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
    # ... Add more test cases as needed
])
def test_identify_word(sentence: str, expected_output: str) -> None:
    result = identify_first_word(sentence)
    something = ParsedWord("aoeu", "aoeu")
    print(result)
    assert result == expected_output
