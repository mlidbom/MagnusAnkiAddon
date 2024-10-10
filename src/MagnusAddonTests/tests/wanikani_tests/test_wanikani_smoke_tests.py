from typing import Generator

import pytest

from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from wanikani import wanikani_api_client

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield


def test_fetch_data_doesnt_crash() -> None:
    client = wanikani_api_client.WanikaniClient.get_instance()

    kana_vocab = client.list_kana_vocabulary()