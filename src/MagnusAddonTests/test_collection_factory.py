import os
import shutil
import threading
from contextlib import contextmanager
from typing import Generator
from anki.collection import Collection
import tempfile
from os import path

from ankiutils import anki_shim
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_collection() -> Collection:
    return checked_cast(Collection, _thread_local.anki_collection)

@contextmanager
def replace_anki_collection_for_testing() -> Generator[None, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        collection = create_collection(collection_file)
        _thread_local.anki_collection = collection
        anki_shim.facade.anki_collection = get_thread_local_collection  # type: ignore
        yield

        collection.close()

def create_collection(collection_file_path: str) -> Collection:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(script_dir, "collection.anki2")
    shutil.copyfile(source_file, collection_file_path)
    print()
    print(source_file)
    print(collection_file_path)

    return Collection(collection_file_path)
