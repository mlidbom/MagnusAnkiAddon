import re
from typing import Generator
import pytest
from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from fixtures.stub_factory import stub_ui_dependencies
from note.vocabnote import VocabNote

@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), inject_empty_anki_collection_with_note_types()):
        yield

@pytest.mark.parametrize('question, answer, readings, forms', [
    ("らっしゃい", "please-come", ["らっしゃい"], ["らっしゃい", "[[らっしゃる]]"])
])
def test_excluded_forms(question:str, answer:str, readings:list[str], forms:set[str]) -> None:
    note = VocabNote.create(question, answer, readings)
    note.set_forms(forms)
    forms_list = list(note.get_forms())
    assert len(forms_list) == 1
    assert forms_list[0] == "らっしゃい"

    excluded_forms_list = list(note.get_excluded_forms())
    assert len(excluded_forms_list) == 1
    assert excluded_forms_list[0] == "らっしゃる"

def test_blah() -> None:
    _forms_exclusions = re.compile(r'\[\[.*]]')

    assert bool(_forms_exclusions.search("[[らっしゃる]]"))