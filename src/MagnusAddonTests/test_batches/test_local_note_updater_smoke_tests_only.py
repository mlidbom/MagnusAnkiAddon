from typing import Generator
import pytest

from batches import local_note_updater
from fixtures.stub_factory import stub_ui_utils
from fixtures.test_collection_factory import inject_empty_anki_collection_with_note_types, inject_anki_collection_with_generated_sample_data
from note.sentencenote import SentenceNote


@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (inject_anki_collection_with_generated_sample_data(), stub_ui_utils()):
        yield


def test_smoke_update_all() -> None:
    local_note_updater.update_all()