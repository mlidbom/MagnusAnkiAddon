import tempfile
import unittest.mock
from contextlib import contextmanager
from os import path
from typing import Generator

from anki.collection import Collection
from fixtures.base_data import note_type_factory
from fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_spec
from fixtures.stub_factory import stub_ui_dependencies
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote




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
        finally:
            anki_collection.close()


def populate_collection(collection: Collection) -> None:
    note_type_factory.add_note_types(collection)

@contextmanager
def inject_anki_collection_with_generated_sample_data() -> Generator[None, None, None]:
    from ankiutils import app
    with inject_empty_anki_collection_with_note_types():
        for kanji in kanji_spec.test_kanji_list:
            KanjiNote.create(kanji.question, kanji.answer, kanji.on_readings, kanji.kun_reading)

        for sentence in sentence_spec.test_sentence_list:
            SentenceNote.create_test_note(sentence.question, sentence.answer)

        for vocab in vocab_spec.test_vocab_list:
            VocabNote.create(vocab.question, vocab.answer, vocab.readings)

        app.col().flush_cache_updates()

        yield
        app.col().destruct()