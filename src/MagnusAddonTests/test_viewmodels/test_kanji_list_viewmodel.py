from typing import Generator

import pytest

from note import jp_collection
from fixtures.test_collection_factory import replace_anki_collection_for_testing
from viewmodels.kanji_list import sentence_kanji_list_viewmodel

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with replace_anki_collection_for_testing():
        yield


def test_kanji_list_viewmodel() -> None:
    sentences = jp_collection.list_sentence_notes()[:1]
    for sentence in sentences:
        view_model = sentence_kanji_list_viewmodel.create(sentence.extract_kanji())
        print()
        print(sentence.get_active_question())
        print(view_model)