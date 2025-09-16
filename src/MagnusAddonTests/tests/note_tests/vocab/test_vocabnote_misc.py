from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_empty_collection
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Iterator

    from note.collection.jp_collection import JPCollection


@pytest.fixture(scope="module", autouse=True)
def empty_collection() -> Iterator[JPCollection]:
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
    print(vocab.readings.get())


def test_perfect_synonyms() -> None:
    first = VocabNote.factory.create("first", "", [])
    second = VocabNote.factory.create("second", "", [])
    third = VocabNote.factory.create("third", "", [])

    first.related_notes.perfect_synonyms.add(second.get_question())
    first.related_notes.perfect_synonyms.add(third.get_question())

    first.user.answer.set("synced_answer")
