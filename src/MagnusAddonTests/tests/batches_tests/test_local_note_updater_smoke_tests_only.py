from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_anki_collection_with_all_sample_data
from fixtures.stub_factory import stub_ui_dependencies

if TYPE_CHECKING:
    from collections.abc import Generator

# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), inject_anki_collection_with_all_sample_data()):
        yield

def test_smoke_full_rebuild(setup: object) -> None:
    from batches import local_note_updater
    local_note_updater.full_rebuild()
