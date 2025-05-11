from collections.abc import Generator

import pytest
from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from wanikani import wanikani_api_client


# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield


@pytest.mark.skip("Really, fetching a ton of data from wanikani every time I run the tests is a bit overboard...")
def test_fetch_data_doesnt_crash() -> None:
    client = wanikani_api_client.WanikaniClient.get_instance()

    kana_vocab = client.list_kana_vocabulary()

    for vocab in kana_vocab:
        print(vocab.characters)