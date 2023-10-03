from typing import Generator
import pytest

from batches import local_note_updater
from fixtures.stub_factory import stub_ui_utils
from fixtures.empty_test_collection_factory import inject_empty_anki_collection_with_note_types
from note.sentencenote import SentenceNote

_sentences = ["駅前にクレープ屋さんができたんだって", "香織　お父さんがケーキ買ってきたよ", "長谷くんは　友達と遊びに行くとしたら　どこ行くの", "長谷くんとの記憶は　全部消えちゃう", "長谷　お前このままじゃ数学の単位落とすぞ"]
def add_some_notes() -> None:
    for sentence_text in _sentences:
        SentenceNote.create(sentence_text)

@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (inject_empty_anki_collection_with_note_types(), stub_ui_utils()):
        add_some_notes()
        yield


def test_smoke_update_all() -> None:
    local_note_updater.update_all()