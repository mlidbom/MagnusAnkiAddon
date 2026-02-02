from __future__ import annotations

import os
import shutil
import tempfile
import unittest.mock
from contextlib import contextmanager
from os import path
from typing import TYPE_CHECKING

from anki.collection import Collection

if TYPE_CHECKING:
    from collections.abc import Iterator


@contextmanager
def inject_full_anki_collection_for_testing() -> Iterator[None]:
    from jastudio.note.collection.anki_jp_collection import AnkiJPCollection
    jp_collection: AnkiJPCollection
    def get_jp_collection() -> AnkiJPCollection: return jp_collection

    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = create_collection(collection_file)
        jp_collection = AnkiJPCollection(anki_collection)
        try:
            with unittest.mock.patch("ankiutils.app.col", new=get_jp_collection):
                yield
        finally:
            anki_collection.close()

def create_collection(collection_file_path: str) -> Collection:
    script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\")
    source_file = os.path.join(script_dir, "collection.anki2")
    shutil.copyfile(source_file, collection_file_path)

    return Collection(collection_file_path)