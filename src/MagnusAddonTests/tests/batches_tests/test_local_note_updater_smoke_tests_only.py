from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jaslib_tests.fixtures.collection_factory import inject_collection_with_all_sample_data

if TYPE_CHECKING:
    from collections.abc import Iterator


# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup() -> Iterator[None]:
    with (inject_collection_with_all_sample_data()):
        yield

@pytest.mark.usefixtures("setup")
def test_smoke_full_rebuild() -> None:
    from jaslib.batches import local_note_updater
    local_note_updater.full_rebuild()
