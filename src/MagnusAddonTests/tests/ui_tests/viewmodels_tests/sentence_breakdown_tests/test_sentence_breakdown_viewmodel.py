from __future__ import annotations

from typing import Generator, TypeAlias

import pytest

from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_generated_sample_data
from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
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
    ("一度夢を見た", SB(N("一度", "", V("一度", "", "", "once/on-one-occation")), N("夢を", "", N("夢", "", V("夢", "", "", "dream")), N("を", "", V("を", "", "", "{marks: direct-object | subject(caus:expr)}"))), N("見た", "", N("見", "見る", V("見", "見る", "", "to{}: see/look | examine | aux{try}"), V("見", "見る", "みる", "to: aux: try/have-a-go-at | {see/find}-that"), V("見", "見る", "観る", "To View, To Watch, To See")), N("た", "", V("た", "", "", "{past-tense} | (please)do"))))),
    ("そっちへ行ったぞ", SB(N("そっちへ", "", N("そっち", "", V("そっち", "", "", "---")), N("へ", "", V("へ", "", "", "---"))), N("行った", "", N("行っ", "行く", V("行っ", "行く", "", "to: go(wide.lit.fig)")), N("た", "", V("た", "", "", "{past-tense} | (please)do"))), N("ぞ", "", V("ぞ", "", "", "---")))),
    #todo: the V("たら", "た"... is bad
    ("だったら", SB(N("だったら", "", V("だったら", "", "", "---"), N("だっ", "だ", V("だっ", "だ", "", "cop{be/is} aux{past-tense | please/do}")), N("たら", "", V("たら", "", "", "conj{if/when} prt{as-for | why-not..  | I-said!/I-tell-you!}"))))),
    ("気づかなかった", SB(N("気づかなかった", "", N("気づか", "気づく", V("気づか", "気づく", "", "to: notice/realize | come-to-one's-senses"), V("気づか", "気づく", "気付く", "to: realize/notice")), N("なかっ", "ない", V("なかっ", "ない", "無い", "{negation} | nonexistent | unowned | impossible/won't-happen")), N("た", "", V("た", "", "", "{past-tense} | (please)do"))))),
    ("出しといて", SB(N("出しといて", "", N("出しとい", "", N("出し", "出す", V("出し", "出す", "", "---")), N("とい", "とく", V("とい", "とく", "", "---"))), N("て", "", V("て", "", "", "{continuing-action}"), V("て", "", "って", "{quotes(speech|thoughts|implications)} | {topic-marker}"))))),
    ("してた", SB(N("してた", "", N("し", "する", V("し", "する", "", "{verbalizes-noun} #to: do | make-into | serve-as | wear")), N("て", "てる", V("て", "てる", "", "{continuing-{activity | state}} / {progressive | perfect}")), N("た", "", V("た", "", "", "{past-tense} | (please)do"))))),
    ("私に日記を書くように言ったのも自分が楽をするためでした", SB(N("私に", "", N("私", "", V("私", "", "", "I/me")), N("に", "", V("に", "", "", "{location/direction/target/reason/purpose} {adv}"))), N("日記を", "", N("日記", "", V("日記", "", "", "diary/journal")), N("を", "", V("を", "", "", "{marks: direct-object | subject(caus:expr)}"))), N("書くように", "", N("書く", "", V("書く", "", "", "to{}: write")), N("ように", "", V("ように", "", "様に", "in-order-to | {hoping/wishing}-that"), N("よう", "", V("よう", "", "様", "appearing/looking | way to | form/style")), N("に", "", V("に", "", "", "{location/direction/target/reason/purpose} {adv}")))), N("言ったのも", "", N("言っ", "言う", V("言っ", "言う", "", "to: say | name/call")), N("たのも", "", N("た", "", V("た", "", "", "{past-tense} | (please)do")), N("の", "", V("の", "", "", "{possesive/attributive} | {nominalizing} | {explanatory} | {subject(sub.phr)}")), N("も", "", V("も", "", "", "prt: too/also | even/as-far-as | even-{if/though} | further/more")))), N("自分が", "", N("自分", "", V("自分", "", "", "{subject's}self, {topics's}self")), N("が", "", V("が", "", "", "{subject} | passive:{object} | but/however/still"))), N("楽を", "", N("楽", "", V("楽", "", "", "comfort/ease/relief | easy/without-hardship")), N("を", "", V("を", "", "", "{marks: direct-object | subject(caus:expr)}"))), N("する", "", V("する", "", "", "{verbalizes-noun} #to: do | make-into | serve-as | wear")), N("ためでした", "", N("ため", "", V("ため", "", "為", "sake/purpose/objective | good/advantage")), N("でし", "です", V("でし", "です", "", "polite-copula{be/is}")), N("た", "", V("た", "", "", "{past-tense} | (please)do")))))
])
def test_sentence_breakdown_viewmodel(sentence: str, expected: SentenceBreakdownViewModelSpec) -> None:
    sentence_note: SentenceNote = SentenceNote.create(sentence, "")
    question = sentence_note.get_question()
    tree = ud_tree_builder.build_tree(ud_parsers.best, question)
    print()
    print(tree)
    view_model = sentence_breakdown_viewmodel.create(tree, app.col())

    result = SentenceBreakdownViewModelSpec.from_view_model(view_model)

    print(f"""
expected: 
{expected}

result:
{result}

result single line for use in @pytest.mark.parametrize:
{result.repr_single_line()}""")

    assert result == expected
