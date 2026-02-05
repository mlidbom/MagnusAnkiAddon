from __future__ import annotations

import tempfile
import unittest.mock
from contextlib import contextmanager
from os import path
from typing import TYPE_CHECKING

from anki.collection import Collection
from jastudio_tests.fixtures.base_data import note_type_factory
from jastudio_tests.fixtures.stub_factory import stub_ui_dependencies

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jastudio.note.collection.anki_jp_collection_syncer import AnkiJPCollectionSyncer as JPLegacyCollection

@contextmanager
def inject_empty_collection() -> Iterator[JPLegacyCollection]:
    from jastudio.note.collection.anki_jp_collection_syncer import AnkiJPCollectionSyncer as JPLegacyCollection2
    jp_legacy_collection: JPLegacyCollection2
    def get_legacy_jp_collection() -> JPLegacyCollection2: return jp_legacy_collection

    with (tempfile.TemporaryDirectory() as tmp_dirname, stub_ui_dependencies()):
        collection_file = path.join(tmp_dirname, "collection.anki2")
        anki_collection = Collection(collection_file)
        try:
            populate_collection(anki_collection)
            jp_legacy_collection = JPLegacyCollection2(anki_collection)
            with unittest.mock.patch("jastudio.ankiutils.app.col", new=get_legacy_jp_collection):
                yield jp_legacy_collection
                jp_legacy_collection.destruct_sync()
        finally:
            anki_collection.close()

def populate_collection(collection: Collection) -> None:
    note_type_factory.add_note_types(collection)