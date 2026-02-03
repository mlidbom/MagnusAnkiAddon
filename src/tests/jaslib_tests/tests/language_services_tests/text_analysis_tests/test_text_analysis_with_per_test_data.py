from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib_tests.fixtures.collection_factory import inject_collection_with_select_data

if TYPE_CHECKING:
    from collections.abc import Iterator

@pytest.fixture(scope="function")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("金<wbr>貸せって", ["金", "貸す", "え", "って"])
])
def test_invisible_space_breakup(sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create_test_note(sentence, "")
    root_words = [w.parsed_form for w in sentence_note.parsing_result.get().parsed_words]
    assert root_words == expected_output