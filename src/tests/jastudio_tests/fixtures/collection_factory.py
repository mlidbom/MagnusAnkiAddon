from __future__ import annotations

import tempfile
import unittest.mock
from contextlib import contextmanager
from os import path
from typing import TYPE_CHECKING

from anki.collection import Collection
from jaslib.note.kanjinote import KanjiNote
from jaslib.note.sentences.sentencenote import SentenceNote
from jastudio.ankiutils import app
from jastudio_tests.fixtures.base_data import note_type_factory
from jastudio_tests.fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_lists
from jastudio_tests.fixtures.stub_factory import stub_ui_dependencies

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jastudio.note.collection.jp_collection import JPCollection as JPLegacyCollection

@contextmanager
def inject_empty_collection() -> Iterator[JPLegacyCollection]:
    from jastudio.note.collection.jp_collection import JPCollection as JPLegacyCollection
    jp_legacy_collection: JPLegacyCollection
    def get_legacy_jp_collection() -> JPLegacyCollection: return jp_legacy_collection

    from jaslib.note.collection.jp_collection import JPCollection
    jp_collection: JPCollection
    def get_jp_collection() -> JPCollection: return jp_collection
    jp_collection = JPCollection()

    with (tempfile.TemporaryDirectory() as tmp_dirname, stub_ui_dependencies()):
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = Collection(collection_file)
        try:
            populate_collection(anki_collection)
            jp_legacy_collection = JPLegacyCollection(anki_collection)
            with unittest.mock.patch("jaslib.app.col", new=get_jp_collection), unittest.mock.patch("jastudio.ankiutils.app.col", new=get_legacy_jp_collection):
                yield jp_legacy_collection
                jp_legacy_collection.destruct_sync()
        finally:
            anki_collection.close()

def populate_collection(collection: Collection) -> None:
    note_type_factory.add_note_types(collection)

@contextmanager
def inject_collection_with_select_data(kanji: bool = False, special_vocab: bool = False, sentences: bool = False) -> Iterator[JPLegacyCollection]:
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

        app.col().flush_cache_updates()

        yield collection

@contextmanager
def inject_collection_with_all_sample_data() -> Iterator[JPLegacyCollection]:
    with inject_collection_with_select_data(kanji=True, special_vocab=True, sentences=True) as collection:
        yield collection
