import os
import shutil
import threading
from contextlib import contextmanager
from typing import Generator
from anki.collection import Collection
import tempfile
from os import path

from ankiutils import app
from note.collection.jp_collection import JPCollection
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_collection() -> JPCollection:
    return checked_cast(JPCollection, _thread_local.jp_collection)

@contextmanager
def inject_full_anki_collection_for_testing() -> Generator[None, None, None]:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = create_collection(collection_file)
        jp_collection = JPCollection(anki_collection)
        try:
            _thread_local.jp_collection = jp_collection
            app.col = get_thread_local_collection
            yield
        finally:
            anki_collection.close()

def create_collection(collection_file_path: str) -> Collection:
    script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\")
    source_file = os.path.join(script_dir, "collection.anki2")
    shutil.copyfile(source_file, collection_file_path)
    print()
    print(source_file)
    print(collection_file_path)

    return Collection(collection_file_path)