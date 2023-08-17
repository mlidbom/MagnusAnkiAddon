import pytest

from parsing.janomeutils import extract_dictionary_forms
from parsing.textparser import ParsedWord, identify_first_word, identify_words2


@pytest.mark.parametrize('sentence, expected_output', [
    ("走る", [ParsedWord('走る', '')]),
    ("走って", [ParsedWord('走る', ''), ParsedWord('て', '')]),
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
      ParsedWord('う', '')]
     )
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
