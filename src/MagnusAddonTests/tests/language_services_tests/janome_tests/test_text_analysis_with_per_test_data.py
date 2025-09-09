from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_anki_collection_with_select_data
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.sentencenote import SentenceNote

if TYPE_CHECKING:
    from collections.abc import Iterator

@pytest.fixture(scope="function")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_anki_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.parametrize("sentence, expected_output", [
    ("金<wbr>貸せって", ["金", "貸す", "って"])
])
def test_invisible_space_breakup(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create_test_note(sentence, "")
    root_words = [w.word for w in sentence_note.parsing_result.get().parsed_words]
    assert root_words == expected_output