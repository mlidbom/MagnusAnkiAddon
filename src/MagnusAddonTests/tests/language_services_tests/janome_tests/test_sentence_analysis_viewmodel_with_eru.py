from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.base_data.sample_data import vocab_spec
from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from tests.language_services_tests.janome_tests.test_sentence_analysis_viewmodel_common import _run_assertions

if TYPE_CHECKING:
    from collections.abc import Iterator

@pytest.fixture(scope="module")
def inject_empty_collection_with_eru() -> Iterator[None]:
    with inject_empty_anki_collection_with_note_types():
        [eru for eru in vocab_spec.test_special_vocab if eru.question == "える"][0].create_vocab_note()
        app.col().flush_cache_updates()
        yield

@pytest.mark.parametrize("sentence, excluded, expected_output", [
    ("会える", [], ["会う", "える"]),
    ("会える", [WordExclusion.global_("会える")], ["会う", "える"]),
    ("会えて", [WordExclusion.global_("会える")], ["会う", "える", "て"]),
    ("作れる", [], ["作る", "える"]),
    ("作れる", [WordExclusion.global_("作れる")], ["作る", "える"]),
    ("作れて", [], ["作る", "える", "て"]),
    ("作れて", [WordExclusion.global_("作れる")], ["作る", "える", "て"]),
    ("今日会えた", [], ["今日", "会う", "える", "た"]),
    ("今日会えた", [WordExclusion.global_("会える")], ["今日", "会う", "える", "た"]),
    ("今日会えないかな", [], ["今日", "会う", "える", "ないか", "な"]),
    ("今日会えないかな", [WordExclusion.global_("会える")], ["今日", "会う", "える", "ないか", "な"]),
    ("この夏は　たくさん思い出を作れたなぁ", [], ["この", "夏", "は", "たくさん", "思い出", "を", "作る", "える", "た", "なぁ"]),
    ("買えよ　私", [], ["買えよ", "私"]),
    ("覚ませない", [], ["覚ます", "える", "ない"])
])
def test_potential_verb_splitting_without_vocab(inject_empty_collection_with_eru: object, sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    _run_assertions(sentence, excluded, expected_output)

