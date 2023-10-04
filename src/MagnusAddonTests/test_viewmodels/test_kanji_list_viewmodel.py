from typing import Generator

import pytest

from ankiutils import app
from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from viewmodels.kanji_list import sentence_kanji_list_viewmodel

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield


def test_kanji_list_viewmodel() -> None:
    sentences = app.col().sentences.all()[:1]
    for sentence in sentences:
        view_model = sentence_kanji_list_viewmodel.create(sentence.extract_kanji())
        print()
        print(sentence.get_active_question())
        print(view_model)