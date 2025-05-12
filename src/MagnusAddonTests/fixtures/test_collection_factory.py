from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_spec
from fixtures.base_data.sample_data.kanji_spec import KanjiSpec
from fixtures.base_data.sample_data.sentence_spec import SentenceSpec
from fixtures.base_data.sample_data.vocab_spec import VocabSpec
from fixtures.collection_factory import inject_anki_collection_with_all_sample_data

if TYPE_CHECKING:
    from collections.abc import Generator

    from note.kanjinote import KanjiNote
    from note.sentencenote import SentenceNote
    from note.vocabnote import VocabNote

# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_all_sample_data():
        yield


def test_kanji_added_correctly() -> None:
    kanji_all:list[KanjiNote] = app.col().kanji.all()
    saved_kanji = [KanjiSpec(kanji.get_question(), kanji.get_answer(), kanji.get_reading_kun_html(), kanji.get_reading_on_html()) for kanji in kanji_all]
    assert set(kanji_spec.test_kanji_list) == set(saved_kanji)

def test_vocab_added_correctly() -> None:
    expected_vocab:set[VocabSpec] = set(vocab_spec.test_vocab_list)
    vocab_all:list[VocabNote] = app.col().vocab.all()
    saved_vocab = set(VocabSpec(vocab.get_question(), vocab.get_answer(), vocab.get_readings()) for vocab in vocab_all)
    assert expected_vocab == saved_vocab

def test_sentences_added_correctly() -> None:
    expected_sentences = sorted(sentence_spec.test_sentence_list, key=lambda x: x.question)
    sentences_all:list[SentenceNote] = sorted(app.col().sentences.all(), key=lambda x: x.get_question())
    saved_vocab = [SentenceSpec(sentence.get_question(), sentence.get_answer()) for sentence in sentences_all]
    assert expected_sentences == saved_vocab