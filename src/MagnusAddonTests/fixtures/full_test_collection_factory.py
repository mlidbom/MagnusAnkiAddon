import os
import shutil
import tempfile
import unittest.mock
from contextlib import contextmanager
from os import path
from typing import Generator

from anki.collection import Collection




@contextmanager
def inject_full_anki_collection_for_testing() -> Generator[None, None, None]:
    from note.collection.jp_collection import JPCollection
    jp_collection: JPCollection
    def get_jp_collection() -> JPCollection: return jp_collection

    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = create_collection(collection_file)
        jp_collection = JPCollection(anki_collection)
        try:
            with unittest.mock.patch('ankiutils.app.col', new=get_jp_collection):
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