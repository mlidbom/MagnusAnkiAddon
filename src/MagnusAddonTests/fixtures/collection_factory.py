import tempfile
import threading
from contextlib import contextmanager
from os import path
from typing import Generator

from anki.collection import Collection

from ankiutils import anki_shim
from fixtures.base_data import note_type_factory
from fixtures.base_data.sample_data import kanji_spec, sentence_spec, vocab_spec
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_collection() -> Collection:
    return checked_cast(Collection, _thread_local.anki_collection)


@contextmanager
def inject_empty_anki_collection_with_note_types() -> Generator[None, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        collection = Collection(collection_file)
        try:
            populate_collection(collection)
            _thread_local.anki_collection = collection
            anki_shim.facade.anki_collection = get_thread_local_collection  # type: ignore
            yield
        finally:
            collection.close()


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