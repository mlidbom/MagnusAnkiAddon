from typing import Generator

import pytest

from ankiutils import app
from fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_spec
from fixtures.base_data.sample_data.kanji_spec import KanjiSpec
from fixtures.base_data.sample_data.sentence_spec import SentenceSpec
from fixtures.base_data.sample_data.vocab_spec import VocabSpec
from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_generated_sample_data():
        yield


def test_kanji_added_correctly() -> None:
    expected_kanji = set(kanji_spec.test_kanji_list)
    saved_kanji = set(KanjiSpec(k.get_question(), k.get_active_answer(), k.get_reading_kun(), k.get_reading_on()) for k in app.col().kanji.all())
    assert expected_kanji == saved_kanji

def test_vocab_added_correctly() -> None:
    expected_vocab = set(vocab_spec.test_vocab_list)
    saved_vocab = set(VocabSpec(k.get_question(), k.get_active_answer(), k.get_readings()) for k in app.col().vocab.all())
    assert expected_vocab == saved_vocab

def test_sentences_added_correctly() -> None:
    expected_sentences = set(sentence_spec.test_sentence_list)
    saved_vocab = set(SentenceSpec(k.get_active_question(), k.get_active_answer()) for k in app.col().sentences.all())
    assert expected_sentences == saved_vocab