from __future__ import annotations

import tempfile
import unittest.mock
from contextlib import contextmanager
from os import path
from typing import TYPE_CHECKING

from anki.collection import Collection
from fixtures.base_data import note_type_factory
from fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_spec
from fixtures.stub_factory import stub_ui_dependencies
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote

if TYPE_CHECKING:
    from collections.abc import Generator


@contextmanager
def inject_empty_anki_collection_with_note_types() -> Generator[None, None, None]:
    from note.collection.jp_collection import JPCollection
    jp_collection: JPCollection
    def get_jp_collection() -> JPCollection: return jp_collection

    with (tempfile.TemporaryDirectory() as tmp_dirname, stub_ui_dependencies()):
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = Collection(collection_file)
        try:
            populate_collection(anki_collection)
            jp_collection = JPCollection(anki_collection)
            with unittest.mock.patch('ankiutils.app.col', new=get_jp_collection):
                yield
                jp_collection.destruct()
        finally:
            anki_collection.close()


def populate_collection(collection: Collection) -> None:
    note_type_factory.add_note_types(collection)

@contextmanager
def inject_anki_collection_with_select_data(kanji:bool = False, special_vocab:bool = False, ordinary_vocab: bool = False, sentences:bool = False) -> Generator[None, None, None]:
    from ankiutils import app
    with inject_empty_anki_collection_with_note_types():
        if kanji:
            for _kanji in kanji_spec.test_kanji_list:
                KanjiNote.create(_kanji.question, _kanji.answer, _kanji.on_readings, _kanji.kun_reading)

        if special_vocab:
            for vocab in vocab_spec.test_special_vocab:
                vocab.create_vocab_note()

        if ordinary_vocab:
            for vocab in vocab_spec.test_ordinary_vocab_list:
                vocab.create_vocab_note()

        if sentences:
            for sentence in sentence_spec.test_sentence_list:
                SentenceNote.create_test_note(sentence.question, sentence.answer)


        app.col().flush_cache_updates()

        yield

@contextmanager
def inject_anki_collection_with_all_sample_data() -> Generator[None, None, None]:
    with inject_anki_collection_with_select_data(kanji=True, special_vocab=True, ordinary_vocab=True, sentences=True):
        yield