import threading
from contextlib import contextmanager
from typing import Generator
from anki.collection import Collection
import tempfile
from os import path

from ankiutils import anki_shim
from fixtures.base_data import note_type_factory
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_collection() -> Collection:
    return checked_cast(Collection, _thread_local.anki_collection)


@contextmanager
def inject_empty_anki_collection_with_note_types() -> Generator[None, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        collection = Collection(collection_file)
        populate_collection(collection)
        _thread_local.anki_collection = collection
        anki_shim.facade.anki_collection = get_thread_local_collection  # type: ignore
        yield

        collection.close()


def populate_collection(collection: Collection) -> None:
    note_type_factory.add_note_types(collection)