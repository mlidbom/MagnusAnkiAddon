from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jastudio.ankiutils import query_builder
from jastudio_tests.fixtures.collection_factory import inject_empty_collection
from jastudio.note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Iterator


# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def setup_empty_collection() -> Iterator[None]:
    with inject_empty_collection():
        yield

def test_something() -> None:
    vocab = VocabNote.factory.create("楽しめる", "", [])
    result = query_builder.potentially_matching_sentences_for_vocab(vocab)

    assert result == """note:_japanese_sentence ("Q:*楽しめり*" OR "Q:*楽しめら*" OR "Q:*楽しめれ*" OR "Q:*楽しめっ*" OR "Q:*楽しめ*" OR "Q:*楽しめろ*" OR "Q:*楽しめな*" OR "Q:*楽しめる*")"""
