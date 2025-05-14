from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_all_sample_data
from fixtures.stub_factory import stub_ui_dependencies

if TYPE_CHECKING:
    from collections.abc import Generator

# from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
# from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
# from note.vocabnote import VocabNote

# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), inject_anki_collection_with_all_sample_data()):
        yield


def test_smoke_update_all(setup:object) -> None:
    from batches import local_note_updater
    local_note_updater.update_all()


def test_memory_leak(setup:object) -> None:
    pass
