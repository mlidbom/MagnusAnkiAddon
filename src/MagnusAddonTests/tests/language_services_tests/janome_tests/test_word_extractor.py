import pytest

from language_services.janome_ex.word_extraction.extracted_word import ExtractedWord
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction import word_extractor

_tokenizer:JNTokenizer

@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = JNTokenizer()

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
     [ExtractedWord('走る')]),
    ("走って",
     [ExtractedWord('走る'),
      ExtractedWord('走っ'),
      ExtractedWord('て')]),
    ("これをください。",
     [ExtractedWord('これ'),
      ExtractedWord('を'),
      ExtractedWord('くださる'),
      ExtractedWord('ください')]),
    ("ハート形",
     [ExtractedWord('ハート'),
      ExtractedWord('ハート形'),
      ExtractedWord('形')]),
    ("私が行きましょう。",
     [ExtractedWord('私'),
      ExtractedWord('が'),
      ExtractedWord('行く'),
      ExtractedWord('行き'),
      ExtractedWord('ます'),
      ExtractedWord('ましょ'),
      ExtractedWord('ましょう'),
      ExtractedWord('う')]),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     [ExtractedWord('１'),
      ExtractedWord('１人'),
      ExtractedWord('１人で'),
      ExtractedWord('人'),
      ExtractedWord('で'),
      ExtractedWord('いる'),
      ExtractedWord('時間'),
      ExtractedWord('が'),
      ExtractedWord('これ'),
      ExtractedWord('これほど'),
      ExtractedWord('ほど'),
      ExtractedWord('まで'),
      ExtractedWord('までに'),
      ExtractedWord('に'),
      ExtractedWord('長い'),
      ExtractedWord('長く'),
      ExtractedWord('感じる'),
      ExtractedWord('と'),
      ExtractedWord('とは'),
      ExtractedWord('は')]),
    ("どうやってここを知った。",
     [ExtractedWord('どう'),
      ExtractedWord('どうやって'),
      ExtractedWord('やる'),
      ExtractedWord('やっ'),
      ExtractedWord('て'),
      ExtractedWord('ここ'),
      ExtractedWord('を'),
      ExtractedWord('知る'),
      ExtractedWord('知っ'),
      ExtractedWord('た')]),
    ("声出したら駄目だからね",
     [ExtractedWord('声'),
      ExtractedWord('出す'),
      ExtractedWord('出し'),
      ExtractedWord('た'),
      ExtractedWord('たら'),
      ExtractedWord('駄目'),
      ExtractedWord('だ'),
      ExtractedWord('だから'),
      ExtractedWord('から'),
      ExtractedWord('ね')]),
    ("彼の日本語のレベルは私と同じ位だ。",
     [ExtractedWord('彼'),
      ExtractedWord('彼の'),
      ExtractedWord('の'),
      ExtractedWord('日本語'),
      ExtractedWord('レベル'),
      ExtractedWord('は'),
      ExtractedWord('私'),
      ExtractedWord('と'),
      ExtractedWord('同じ'),
      ExtractedWord('同じ位'),
      ExtractedWord('位'),
      ExtractedWord('だ')]
     )
])
def test_identify_words(sentence: str, expected_output: list[ExtractedWord]) -> None:
    result = word_extractor.extract_words(sentence)
    assert result == expected_output

def test_ignores_noise_characters() -> None:
    result = word_extractor.extract_words(". , : ; / | 。 、 ー")
    assert result == [ExtractedWord("ー")]

def test_something() -> None:
    result = word_extractor.extract_words("知ってる人があんまりいない高校に行って")
    print(result)
