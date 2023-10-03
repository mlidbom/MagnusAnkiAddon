from typing import Generator

import pytest

from ankiutils import search_utils
from fixtures.base_data.sample_data import sentence_spec
from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data
from note import jp_collection
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_generated_sample_data():
        yield


@pytest.mark.parametrize('sentence', [f.question for f in sentence_spec.test_sentence_list])
def test_sentence_breakdown_viewmodel(sentence:str) -> None:
    sentence_note = jp_collection.search_sentence_notes(search_utils.sentence_exact(sentence))[0]
    view_model = sentence_breakdown_viewmodel.create(sentence_note)
    print()
    print(sentence_note.get_active_question())
    print(view_model)