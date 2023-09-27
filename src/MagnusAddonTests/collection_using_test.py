from typing import Generator
import pytest

from ankiutils.anki_shim import facade
from test_collection_factory import replace_anki_collection_for_testing
from wanikani.wani_collection import WaniCollection


@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with replace_anki_collection_for_testing():
        yield


_paths: set[str] = set()
@pytest.mark.parametrize('something', ["string1", "string2", "string3","string4","string5","string6","string7","string8","string9","string10","string11"])
def test_function(something: str) -> None:
    col = facade.col()
    print()
    print(col.path)
    assert col.path not in _paths
    _paths.add(col.path)
    kanji = WaniCollection.fetch_all_wani_kanji_notes()[:10]
    for kan in kanji:
        print(kan.get_question())