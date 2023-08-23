import pytest

from parsing.janome_extensions.parts_of_speech import POS, PartsOfSpeech
from parsing.janome_extensions.tokenizer_ext import TokenizerExt

_tokenizer = TokenizerExt()


@pytest.mark.parametrize('sentence, expected_parts_of_speech', [
    ("こんなに", [POS.Adverb.particle_connection]),
    ("こんなに疲れている", [POS.Adverb.particle_connection, POS.Verb.independent,             POS.Particle.conjunctive, POS.Verb.non_independent]),
    ("こんなに食べている", [POS.Adverb.particle_connection, POS.Verb.independent,             POS.Particle.conjunctive, POS.Verb.non_independent]),
    ("こんなにする",      [POS.pre_noun_adjectival,        POS.Particle.CaseMarking.general, POS.Verb.independent]),
    ("そんなに好きだ",    [POS.Adverb.general,             POS.Noun.na_adjective_stem,       POS.bound_auxiliary]),
    ("こんなに食べる",    [POS.pre_noun_adjectival,        POS.Particle.CaseMarking.general, POS.Verb.independent]),
    ("そんなに走った",    [POS.Adverb.general,             POS.Verb.independent,             POS.bound_auxiliary])
])
def test_identify_something_words(sentence: str, expected_parts_of_speech: list[PartsOfSpeech]) -> None:
    tokenized = _tokenizer.tokenize(sentence)
    parts_of_speech = [tok.parts_of_speech for tok in tokenized.tokens]

    assert expected_parts_of_speech == parts_of_speech
