from __future__ import annotations

from typing import Generator, TypeAlias

import pytest

from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data
from note.sentencenote import SentenceNote
from tests.ui_tests.viewmodels_tests.sentence_breakdown_tests.breakdown_viewmodel_spec import NodeViewModelSpec, SentenceBreakdownViewModelSpec, VocabHitViewModelSpec
from viewmodels.sentence_breakdown import sentence_breakdown_viewmodel

V: TypeAlias = VocabHitViewModelSpec
SB: TypeAlias = SentenceBreakdownViewModelSpec
N: TypeAlias = NodeViewModelSpec

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_generated_sample_data():
        yield

@pytest.mark.parametrize('sentence, expected', [
    ("一度夢を見た", SB(N("一度", "", V("一度", "", "", "once/on-one-occation")), N("夢を見た", "夢を見る", V("夢を見た", "夢を見る", "", "to: dream"), N("夢を", "", N("夢", "", V("夢", "", "", "dream")), N("を", "", V("を", "", "", "{marks: direct-object | subject(caus:expr)}"))), N("見た", "", N("見", "見る", V("見", "", "", "---"), V("見", "見る", "", "to{}: see/look | examine | aux{try}"), V("見", "見る", "みる", "to: aux: try/have-a-go-at | {see/find}-that"), V("見", "見る", "観る", "To View, To Watch, To See")), N("た", "", V("た", "", "", "{past-tense} | (please)do")))))),
    ("そっちへ行ったぞ", SB(N("そっちへ", "", N("そっち", "", V("そっち", "", "", "---")), N("へ", "", V("へ", "", "", "---"))), N("行ったぞ", "", N("行っ", "行く", V("行っ", "行く", "", "to: go(wide.lit.fig)")), N("た", "", V("た", "", "", "{past-tense} | (please)do")), N("ぞ", "", V("ぞ", "", "", "---"))))),
    ("だったら", SB(N("だったら", "", V("だったら", "", "", "---"), N("だっ", "だ"), N("たら", "た", V("たら", "", "", "conj{if/when} prt{as-for | why-not..  | I-said!/I-tell-you!}"))))),

])
def test_sentence_breakdown_viewmodel(sentence: str, expected: SentenceBreakdownViewModelSpec) -> None:
    sentence_note: SentenceNote = SentenceNote.create(sentence, "")
    view_model = sentence_breakdown_viewmodel.create(sentence_note, app.col())

    result = SentenceBreakdownViewModelSpec.from_view_model(view_model)

    print(f"""
expected: 
{expected}

result:
{result}

result single line for use in @pytest.mark.parametrize:
{result.repr_single_line()}""")

    assert result == expected
