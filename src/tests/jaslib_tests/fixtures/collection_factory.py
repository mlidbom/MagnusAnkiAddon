from __future__ import annotations

import unittest.mock
from contextlib import contextmanager
from typing import TYPE_CHECKING

from jaslib.note.kanjinote import KanjiNote
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib_tests.fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_lists

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jaslib.note.collection.jp_collection import JPCollection

@contextmanager
def inject_empty_collection() -> Iterator[JPCollection]:
    from jaslib.note.collection.jp_collection import JPCollection
    jp_collection: JPCollection
    def get_jp_collection() -> JPCollection: return jp_collection


    jp_collection = JPCollection()
    with unittest.mock.patch("jaslib.app.col", new=get_jp_collection):
        yield jp_collection
        jp_collection.destruct_sync()


@contextmanager
def inject_collection_with_select_data(kanji: bool = False, special_vocab: bool = False, sentences: bool = False) -> Iterator[JPCollection]:
    with inject_empty_collection() as collection:
        if kanji:
            for _kanji in kanji_spec.test_kanji_list:
                KanjiNote.create(_kanji.question, _kanji.answer, _kanji.on_readings, _kanji.kun_reading)

        if special_vocab:
            for vocab in vocab_lists.test_special_vocab:
                vocab.create_vocab_note()

        if sentences:
            for sentence in sentence_spec.test_sentence_list:
                SentenceNote.create_test_note(sentence.question, sentence.answer)

        yield collection

@contextmanager
def inject_collection_with_all_sample_data() -> Iterator[JPCollection]:
    with inject_collection_with_select_data(kanji=True, special_vocab=True, sentences=True) as collection:
        yield collection
