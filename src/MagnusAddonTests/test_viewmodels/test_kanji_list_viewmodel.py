from typing import Generator

import pytest

from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data, inject_empty_anki_collection_with_note_types
from viewmodels.kanji_list import sentence_kanji_list_viewmodel

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_generated_sample_data():
        yield


def test_kanji_list_viewmodel() -> None:
    sentences = app.col().sentences.all()[:10]
    for sentence in sentences:
        extracted_kanji = sentence.extract_kanji()
        view_model = sentence_kanji_list_viewmodel.create(extracted_kanji)
        print()
        print(sentence.get_active_question())
        print(view_model)

        extracted_kanji_set = set(extracted_kanji)
        found_kanji_set = set( m.question() for m in view_model.kanji_list )

        print(f"""{len(extracted_kanji_set)}:{len(found_kanji_set)}""")

        assert found_kanji_set == extracted_kanji_set