from typing import Generator
import pytest

from ankiutils.anki_shim import facade
from fixtures.test_collection_factory import inject_empty_anki_collection_with_note_types
from note import jp_collection


@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield


_paths: set[str] = set()
@pytest.mark.parametrize('something', ["string1", "string2", "string3","string4","string5","string6","string7","string8","string9","string10","string11"])
def test_function(something: str) -> None:
    collection = facade.anki_collection()
    print()
    print(collection.path)
    assert collection.path not in _paths
    _paths.add(collection.path)
    kanji = jp_collection.fetch_all_wani_kanji_notes()[:10]
    for kan in kanji:
        print(kan.get_question())