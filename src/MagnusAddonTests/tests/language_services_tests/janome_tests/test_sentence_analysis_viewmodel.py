from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.base_data.sample_data import vocab_spec
from fixtures.collection_factory import inject_anki_collection_with_select_data, inject_empty_anki_collection_with_note_types
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.sentences.sentence_configuration import SentenceConfiguration
from note.sentences.sentencenote import SentenceNote
from sysutils import ex_sequence
from sysutils.lazy import Lazy
from ui.web.sentence.sentence_viewmodel import SentenceAnalysisViewModel

if TYPE_CHECKING:
    from collections.abc import Iterator

# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_anki_collection_with_select_data(special_vocab=True):
        yield

@pytest.fixture(scope="function")
def setup_empty_collection() -> Iterator[None]:
    with inject_empty_anki_collection_with_note_types():
        yield

@pytest.mark.parametrize("sentence, excluded, expected_output", [
    ("厳密に言えば　俺一人が友達だけど",
     [],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど"]),
    ("厳密に言えば　俺一人が友達だけど",
     [WordExclusion.global_("厳密に言えば"), WordExclusion.global_("言え"), WordExclusion.global_("だけど")],
     ["厳密", "に", "言う", "ば", "俺", "一人", "が", "友達", "だ", "けど"]),
    ("厳密に言えば　俺一人が友達だけどだけど",
     [],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど", "だけど"]),
    ("厳密に言えばだけど俺一人が友達だけど",
     [WordExclusion.at_index("だけど", 6)],  # You don't get to exclude tokens, it would mutilate the text, so this will remain.
     ["厳密に言えば", "だけど", "俺", "一人", "が", "友達", "だけど"]),
    ("幼すぎて よく覚えていないけど",
     [],
     ["幼い", "すぎる", "て", "よく", "覚える", "ている", "ない", "けど"]),
    ("私は毎日ジョギングをすることを習慣にしています。",
     [WordExclusion.at_index("にして", 17), WordExclusion.at_index("にし", 17), WordExclusion.at_index("して", 18), WordExclusion.at_index("し", 18), WordExclusion.at_index("してい", 18), WordExclusion.at_index("い", 12), WordExclusion.global_("にする")],
     ["私", "は", "毎日", "ジョギング", "を", "する", "こと", "を", "習慣", "に", "する", "ている", "ます"]),
    ("私は毎日ジョギングをすることを習慣にしています。",
     [WordExclusion.at_index("にして", 17), WordExclusion.at_index("にし", 17), WordExclusion.at_index("して", 18), WordExclusion.at_index("し", 18), WordExclusion.at_index("してい", 18)],
     ["私", "は", "毎日", "ジョギング", "を", "する", "こと", "を", "習慣", "にする", "ている", "ます"]),
    ("ばら撒かれるなんて死んでもいやだ",
     [],
     ["ばら撒く", "あれる", "なんて", "死んでも", "いや", "だ"]),
    ("お前も色々考えてるんだなぁ",
     [],
     ["お前", "も", "色々", "考える", "てる", "んだ", "なぁ"]),
    ("教科書落ちちゃうから",
     [],
     ["教科書", "落ちる", "ちゃう", "から"]),
    ("待ってました", [], ["待つ", "て", "ます", "た"]),
    ("落ちてないかな", [], ["落ちる", "てる", "ないか", "な"]),
    ("分かってたら", [], ["分かる", "てたら"]),
    ("頑張れたというか", [WordExclusion.global_("頑張れ")], ["頑張る", "える", "た", "というか"]),
    ("思い出せそうな気がする", [], ["思い出す", "える", "そうだ", "気がする"]),
    ("いらっしゃいません", [WordExclusion.global_("いらっしゃいませ")], ["いらっしゃいます", "ん"]),
    ("代筆を頼みたいんだが", [], ["代筆", "を", "頼む", "たい", "んだ", "が"]),
    ("飛ばされる", [], ["飛ばす", "あれる"]),
    ("食べれる", [], ["食べる", "れる"]),
    ("破られたか", [], ["破る", "あれる", "たか"]),
    ("大家族だもの", [], ["大家族", "だもの"]),
    ("奪うんだもの", [], ["奪う", "んだ", "もの"]),
    ("難しく考えすぎ", [], ["難しい", "考えすぎ"]),
    ("やり過ぎた", [], ["やり過ぎる", "た"]),
    ("ない", [], ["ない"]),
    ("俺に謝られても", [], ["俺", "に", "謝る", "あれる", "ても"]),
    # ("いいのかよ", [], ["いい", "の", "かよ"]), #todo
    ("立ってるのかと思った", [], ["立つ", "てる", "のか", "と", "思う", "た"]),
])
def test_misc_stuff(setup_collection_with_select_data: object, sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    _run_assertions(sentence, excluded, expected_output)

@pytest.mark.parametrize("sentence, excluded, expected_output", [
    ("会える", [], ["会える"]),
    ("会える", [WordExclusion.global_("会える")], ["会う", "える"]),
    ("会えて", [WordExclusion.global_("会える")], ["会う", "える", "て"]),
    ("作れる", [], ["作れる"]),
    ("作れる", [WordExclusion.global_("作れる")], ["作る", "える"]),
    ("作れて", [], ["作れる", "て"]),
    ("作れて", [WordExclusion.global_("作れる")], ["作る", "える", "て"]),
    ("今日会えた", [], ["今日", "会える", "た"]),
    ("今日会えた", [WordExclusion.global_("会える")], ["今日", "会う", "える", "た"]),
    ("今日会えないかな", [], ["今日", "会える", "ないか", "な"]),
    ("今日会えないかな", [WordExclusion.global_("会える")], ["今日", "会う", "えない", "かな"]),
    ("この夏は　たくさん思い出を作れたなぁ", [], ["この", "夏", "は", "たくさん", "思い出", "を", "作れる", "た", "なぁ"]),
])
def test_potential_verb_splitting_with_vocab(setup_collection_with_select_data: object, sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    _run_assertions(sentence, excluded, expected_output)

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
def test_potential_verb_splitting_without_vocab(setup_empty_collection: object, sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    [eru for eru in vocab_spec.test_special_vocab if eru.question == "える"][0].create_vocab_note()
    app.col().flush_cache_updates()
    _run_assertions(sentence, excluded, expected_output)

def _run_assertions(sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    sentence_note = SentenceNote.create(sentence)
    sentence_note.configuration._value = Lazy.from_value(SentenceConfiguration.from_incorrect_matches(excluded))
    analysis = SentenceAnalysisViewModel(sentence_note)
    candidate_words = analysis.analysis.candidate_words
    display_forms = ex_sequence.flatten([cand.display_forms for cand in candidate_words])
    displayed_forms = [display_form for display_form in display_forms if display_form.is_displayed]

    root_words = [df.parsed_form for df in displayed_forms]
    assert root_words == expected_output
