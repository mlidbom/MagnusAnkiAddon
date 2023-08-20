import pytest
from janome.tokenizer import Tokenizer

from parsing.janome_extensions.parsed_word import ParsedWord
from parsing.textparser import identify_words

_tokenizer = Tokenizer()

#TODO: See if we can't find a way to parse suru out of sentences such that the verbalizing suffix can be
# handled separately from the stand-alone word.
# Now that we have reasonably good POS handling this should be no harder than checking if the previous token
# is a suru verb once we find an instance of suru right?
# It's a word specific hack, but for suru, maybe it is OK since it is one heck of a special word.
#
#
# todo:
#  Check out SudachiPy
#  https://pypi.org/project/SudachiDict-full/
#  https://github.com/polm/fugashi
#  https://github.com/nakagami/janomecabdic
#  https://pypi.org/project/unidic2ud/
#
# def test_suffix_suru_recognized_as_suffix() -> None:
#     result = list(_tokenizer.tokenize("心配する"))
#     print(result)
#     assert result == "NOT HAPPENING"
#
# def test_stand_alone_suru_recognized_as_stand_alone() -> None:
#     result = list(_tokenizer.tokenize("する"))
#     print(result)
#     assert result == "NOT HAPPENING"

@pytest.mark.parametrize('sentence, expected_output', [
    ("走る",
     [ParsedWord('走る')]),
    ("走って",
     [ParsedWord('走る'),
      ParsedWord('て')]),
    ("これをください。",
     [ParsedWord('これ'),
      ParsedWord('を'),
      ParsedWord('くださる'),
      ParsedWord('ください')]),
    ("ハート形",
     [ParsedWord('ハート'),
      ParsedWord('ハート形'),
      ParsedWord('形')]),
    ("私が行きましょう。",
     [ParsedWord('私'),
      ParsedWord('が'),
      ParsedWord('行く'),
      ParsedWord('行き'),
      ParsedWord('ます'),
      ParsedWord('ましょ'),
      ParsedWord('ましょう'),
      ParsedWord('う')]),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     [ParsedWord('１'),
      ParsedWord('１人'),
      ParsedWord('１人で'),
      ParsedWord('人'),
      ParsedWord('で'),
      ParsedWord('いる'),
      ParsedWord('時間'),
      ParsedWord('が'),
      ParsedWord('これ'),
      ParsedWord('これほど'),
      ParsedWord('ほど'),
      ParsedWord('まで'),
      ParsedWord('までに'),
      ParsedWord('に'),
      ParsedWord('長い'),
      ParsedWord('感じる'),
      ParsedWord('と'),
      ParsedWord('とは'),
      ParsedWord('は')]),
    ("どうやってここを知った。",
     [ParsedWord('どう'),
      ParsedWord('どうやって'),
      ParsedWord('やる'),
      ParsedWord('て'),
      ParsedWord('ここ'),
      ParsedWord('を'),
      ParsedWord('知る'),
      ParsedWord('た')]),
    ("声出したら駄目だからね",
     [ParsedWord('声'),
      ParsedWord('出す'),
      ParsedWord('出し'),
      ParsedWord('た'),
      ParsedWord('たら'),
      ParsedWord('駄目'),
      ParsedWord('だ'),
      ParsedWord('だから'),
      ParsedWord('から'),
      ParsedWord('ね')]),
    ("彼の日本語のレベルは私と同じ位だ。",
     [ParsedWord('彼'),
      ParsedWord('彼の'),
      ParsedWord('の'),
      ParsedWord('日本語'),
      ParsedWord('レベル'),
      ParsedWord('は'),
      ParsedWord('私'),
      ParsedWord('と'),
      ParsedWord('同じ'),
      ParsedWord('同じ位'),
      ParsedWord('位'),
      ParsedWord('だ')]
     )
])
def test_identify_words(sentence: str, expected_output: list[ParsedWord]) -> None:
    result = identify_words(sentence)
    print(result)
    assert result == expected_output

def test_ignores_noise_characters() -> None:
    result = identify_words(".,:;/|。、ー")
    print(result)
    assert result == [ParsedWord("ー")]