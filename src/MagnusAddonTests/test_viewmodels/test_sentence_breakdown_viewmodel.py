from typing import Generator

import pytest

from ankiutils import search_utils
from note.jp_collection import JPLegacyCollection
from test_collection_factory import replace_anki_collection_for_testing
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel


@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with replace_anki_collection_for_testing():
        yield



@pytest.mark.parametrize('sentence', [
    "駅前にクレープ屋さんができたんだって",
    "香織　お父さんがケーキ買ってきたよ",
    "長谷くんは　友達と遊びに行くとしたら　どこ行くの",
    "長谷くんとの記憶は　全部消えちゃう",
    "長谷　お前このままじゃ数学の単位落とすぞ"
])
def test_sentence_breakdown_viewmodel(sentence:str) -> None:
    sentences = JPLegacyCollection.search_sentence_notes(search_utils.sentence_exact(sentence))

    assert len(sentences) == 1

    sentence_note = sentences[0]
    view_model = sentence_breakdown_viewmodel.create(sentence_note)
    print()
    print(sentence_note.get_active_question())
    print(view_model)