from __future__ import annotations

import unittest.mock
from contextlib import contextmanager
from typing import TYPE_CHECKING

from jaslib.note.backend_note_creator import TestingBackendNoteCreator

if TYPE_CHECKING:
    from collections.abc import Iterator


@contextmanager
def inject_full_anki_collection_for_testing() -> Iterator[None]:
    from jaslib.note.collection.jp_collection import JPCollection
    jp_collection: JPCollection
    def get_jp_collection() -> JPCollection: return jp_collection

    jp_collection = JPCollection(TestingBackendNoteCreator())

    with unittest.mock.patch("ankiutils.app.col", new=get_jp_collection):
        yield