import tempfile
import threading
from contextlib import contextmanager
from os import path
from typing import Generator

from anki.collection import Collection

from ankiutils import app
from fixtures.base_data import note_type_factory
from fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_spec
from note.collection.jp_collection import JPCollection
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_collection() -> JPCollection:
    return checked_cast(JPCollection, _thread_local.jp_collection)


@contextmanager
def inject_empty_anki_collection_with_note_types() -> Generator[None, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = Collection(collection_file)
        jp_collection = JPCollection(anki_collection)
        try:
            populate_collection(anki_collection)
            _thread_local.jp_collection = jp_collection
            app.col = get_thread_local_collection
            yield
        finally:
            anki_collection.close()


def populate_collection(collection: Collection) -> None:
    note_type_factory.add_note_types(collection)

@contextmanager
def inject_anki_collection_with_generated_sample_data() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        for kanji in kanji_spec.test_kanji_list:
            KanjiNote.create(kanji.question, kanji.answer, kanji.on_readings, kanji.kun_reading)

        for sentence in sentence_spec.test_sentence_list:
            SentenceNote.create(sentence.question, sentence.answer)

        for vocab in vocab_spec.test_vocab_list:
            VocabNote.create(vocab.question, vocab.answer, vocab.readings)

        yield