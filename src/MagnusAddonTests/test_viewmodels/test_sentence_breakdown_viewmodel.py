from typing import Generator

import pytest
from fixtures.test_collection_factory import inject_empty_anki_collection_with_note_types
from note.sentencenote import SentenceNote
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel


@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield


@pytest.mark.parametrize('sentence', [
    "駅前にクレープ屋さんができたんだって",
    "香織　お父さんがケーキ買ってきたよ",
    "長谷くんは　友達と遊びに行くとしたら　どこ行くの",
    "長谷くんとの記憶は　全部消えちゃう",
    "長谷　お前このままじゃ数学の単位落とすぞ"
])
def test_sentence_breakdown_viewmodel(sentence:str) -> None:
    sentence_note = SentenceNote.create(sentence)
    view_model = sentence_breakdown_viewmodel.create(sentence_note)
    print()
    print(sentence_note.get_active_question())
    print(view_model)