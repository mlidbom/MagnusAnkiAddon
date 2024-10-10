from typing import Generator

import pytest

from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data
from fixtures.stub_factory import stub_progress_runner, stub_ui_utils

@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (stub_ui_utils(), stub_progress_runner(), inject_anki_collection_with_generated_sample_data()):
        yield


def test_smoke_update_all() -> None:
    from batches import local_note_updater
    local_note_updater.update_all()