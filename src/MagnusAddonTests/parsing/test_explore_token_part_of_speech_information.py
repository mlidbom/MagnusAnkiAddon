import pytest

from parsing.janome_extensions.parts_of_speech import FullPartsOfSpeech, PartsOfSpeech
from parsing.janome_extensions.tokenizer_ext import TokenizerExt

_tokenizer = TokenizerExt()


@pytest.mark.parametrize('sentence, expected_parts_of_speech', [
    ("こんなに", [FullPartsOfSpeech.Adverb.particle_connection])
])
def test_identify_something_words(sentence: str, expected_parts_of_speech: list[PartsOfSpeech]) -> None:
    tokenized = _tokenizer.tokenize(sentence)
    parts_of_speech = [tok.parts_of_speech for tok in tokenized.tokens]

    assert parts_of_speech == expected_parts_of_speech
