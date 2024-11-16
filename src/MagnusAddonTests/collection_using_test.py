from typing import Generator
import pytest

from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from ankiutils import app

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield


_paths: set[str] = set()
@pytest.mark.parametrize('something', ["string1", "string2", "string3","string4","string5","string6","string7","string8","string9","string10","string11"])
def test_function(something: str) -> None:
    collection = app.anki_collection()
    print()
    print(collection.path)
    assert collection.path not in _paths
    _paths.add(collection.path)
    kanji = app.col().kanji.all_wani()[:10]
    for kan in kanji:
        print(kan.get_question())