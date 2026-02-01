from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.collection_factory import inject_collection_with_all_sample_data
from jaslib.viewmodels.kanji_list import sentence_kanji_list_viewmodel

if TYPE_CHECKING:

    from collections.abc import Iterator

    from jaslib.note.sentences.sentencenote import SentenceNote


# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Iterator[None]:
    with inject_collection_with_all_sample_data():
        yield


def test_kanji_list_viewmodel() -> None:
    sentences:list[SentenceNote] = app.col().sentences.all()
    for sentence in sentences:
        extracted_kanji = sentence.extract_kanji()
        view_model = sentence_kanji_list_viewmodel.create(extracted_kanji)

        extracted_kanji_set = set(extracted_kanji)
        found_kanji_set = {m.question() for m in view_model.kanji_list}

        assert found_kanji_set == extracted_kanji_set