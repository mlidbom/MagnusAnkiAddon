from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.sysutils import ex_str
from jastudio_tests.fixtures.collection_factory import inject_empty_collection
from jastudio_tests.fixtures.stub_factory import stub_ui_dependencies

if TYPE_CHECKING:
    from collections.abc import Iterator


# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup() -> Iterator[None]:
    with (stub_ui_dependencies(), inject_empty_collection()):
        yield

def test_split_token() -> None:
    sentence = "だったら普通に金貸せって言えよ"

    sentence_note = SentenceNote.create(sentence)
    sentence_note.question.split_token_with_word_break_tag("金貸")

    assert sentence_note.question.with_invisible_space() == f"だったら普通に金{ex_str.invisible_space}貸せって言えよ"
