from __future__ import annotations

from typing import Generator, TypeAlias

import pytest

from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data
from note.sentencenote import SentenceNote
from sysutils.stringutils import StringUtils
from test_viewmodels.test_sentence_breakdown.breakdown_viewmodel_spec import NodeViewModelSpec, SentenceBreakdownViewModelSpec
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel

S: TypeAlias = SentenceBreakdownViewModelSpec
N: TypeAlias = NodeViewModelSpec

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_generated_sample_data():
        yield


@pytest.mark.parametrize('sentence, expected', [
    ("一度夢を見た", S(N("一度", ""), N("夢を見た", "", N("夢を", "", N("夢", ""), N("を", "")), N("見た", "", N("見", "見る"), N("た", ""))))),

])
def test_sentence_breakdown_viewmodel(sentence:str, expected: SentenceBreakdownViewModelSpec) -> None:
    sentence_note:SentenceNote = SentenceNote.create(sentence, "")
    view_model = sentence_breakdown_viewmodel.create(sentence_note)

    result = SentenceBreakdownViewModelSpec.from_view_model(view_model)

    print(f"""
expected: 
{expected}

result:
{result}

result single line for use in @pytest.mark.parametrize:
{result.repr_single_line()}""")

    assert expected == result


