from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import pytest
from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from fixtures.stub_factory import stub_ui_dependencies
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Generator

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), inject_empty_anki_collection_with_note_types()):
        yield

def test_blah() -> None:
    _forms_exclusions = re.compile(r"\[\[.*]]")

    assert bool(_forms_exclusions.search("[[らっしゃる]]"))

def test_generate_from_dictionary() -> None:
    vocab = VocabNote.factory.create_with_dictionary("やる気満々")
    assert vocab.get_question() == "やる気満々"
    assert vocab.get_answer() == "totally-willing/fully-motivated"
    assert vocab.readings.get() == ["やるきまんまん"]
    print(vocab.readings.get())
