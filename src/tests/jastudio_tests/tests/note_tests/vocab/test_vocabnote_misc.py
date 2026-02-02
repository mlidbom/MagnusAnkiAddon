from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from jaslib.note.vocabulary.vocabnote import VocabNote
from jastudio_tests.fixtures.collection_factory import inject_empty_collection

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jastudio.note.collection.anki_jp_collection_syncer import AnkiJPCollectionSyncer

# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def empty_collection() -> Iterator[AnkiJPCollectionSyncer]:
    with inject_empty_collection() as collection:
        yield collection

def test_blah() -> None:
    _forms_exclusions = re.compile(r"\[\[.*]]")

    assert bool(_forms_exclusions.search("[[らっしゃる]]"))

def test_generate_from_dictionary() -> None:
    vocab = VocabNote.factory.create_with_dictionary("やる気満々")
    assert vocab.get_question() == "やる気満々"
    assert vocab.get_answer() == "totally-willing/fully-motivated"
    assert vocab.readings.get() == ["やるきまんまん"]