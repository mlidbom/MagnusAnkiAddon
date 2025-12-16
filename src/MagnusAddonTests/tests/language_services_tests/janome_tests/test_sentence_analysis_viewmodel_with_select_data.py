from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_collection_with_select_data
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from tests.language_services_tests.janome_tests.test_sentence_analysis_viewmodel_common import assert_all_words_equal, assert_display_words_equal_and_that_analysis_internal_state_is_valid

if TYPE_CHECKING:
    from collections.abc import Iterator

# noinspection PyUnusedFunction
@pytest.fixture(scope="module")
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("厳密に言えば　俺一人が友達だけど",
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど"]),
    ("厳密に言えば　俺一人が友達だけどだけど",
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど", "だけど"]),
    ("幼すぎて よく覚えていないけど",
     ["幼い", "すぎる", "て", "よく", "覚える", "ている", "ない", "けど"]),
    ("ばら撒かれるなんて死んでもいやだ",
     ["ばら撒く", "あれる", "なんて", "死んでも", "いや", "だ"]),
    ("お前も色々考えてるんだなぁ",
     ["お前", "も", "色々", "考える", "てる", "んだ", "なぁ"]),
    ("教科書落ちちゃうから",
     ["教科書", "落ちる", "ちゃう", "から"]),
    ("待ってました", ["待つ", "て", "ます", "た"]),
    ("落ちてないかな", ["落ちる", "てる", "ないか", "な"]),
    ("分かってたら", ["分かる", "てたら"]),
    ("思い出せそうな気がする", ["思い出す", "える", "そうだ", "気がする"]),
    ("代筆を頼みたいんだが", ["代筆", "を", "頼む", "たい", "ん", "だが"]),
    ("飛ばされる", ["飛ばす", "あれる"]),
    ("食べれる", ["食べる", "れる"]),
    ("破られたか", ["破る", "あれる", "た", "か"]),
    ("大家族だもの", ["大家族", "だもの"]),
    ("奪うんだもの", ["奪う", "ん", "だもの"]),
    ("難しく考えすぎ", ["難しい", "考えすぎ"]),
    ("やり過ぎた", ["やり過ぎる", "た"]),
    ("ない", ["ない"]),
    ("俺に謝られても", ["俺", "に", "謝る", "あれる", "ても"]),
    ("いいのかよ", ["いい", "の", "かよ"]),
    ("立ってるのかと思った", ["立つ", "てる", "のか", "と思う", "た"]),
    ("ないと思う", ["ない", "と思う"]),
    ("しても", ["する", "ても"]),
    ("見えなくなったって そんな", ["見える", "なくなる", "たって", "そんな"]),
    ("焼けたかな", ["焼ける", "た", "かな"]),
    ("何て言うか<wbr>さ", ["何", "て言うか:ていうか", "さ"]),
    ("また来ような", ["また", "来る", "う", "な"]),
    ("何なんだろうな", ["何だ", "ん", "だろう", "な"]),
    ("書きなさい", ["書く", "なさい"]),
    ("存在したね", ["存在", "する", "た", "ね"]),
    ("作るに決まってるだろ", ["作る", "に決まってる", "だろ"]),
    ("知らないんでしょう", ["知らない", "ん", "でしょう"]),
    ("横取りされたらたまらん", ["横取り", "される", "たら", "たまらん"]),
    ("ガチだったんでしょ", ["ガチ", "だった", "ん", "でしょ"]),
    ("どうしちゃったんだろうな", ["どう", "しちゃう", "たん:たの", "だろう", "な"]),
    ("良いものを食べる", ["良い", "もの", "を", "食べる"]),
    ("いいものを食べる", ["いい", "もの", "を", "食べる"]),
    ("うまく笑えずに", ["うまく", "笑える", "ずに"]), # うまく disappeared when we made all verbs inflecting words by default
    ("慣れているんでね", ["慣れる", "ている", "んで", "ね"]),
    ("私が頼んだの", ["私", "が", "頼む", "んだ", "の"]),
    ("月光が差し込んでるんだ", ["月光", "が", "差し込む", "んでる", "んだ"]),
    ("悪かったって", ["悪い", "た", "って"]),
    ("落としたって何を", ["落とす", "た", "って", "何", "を"]),
    ("行ったって話", ["行く", "たって", "話"]),
    ("会いに行ったんだ", ["会う", "に行く", "たんだ"]),
    ("聞こうと思ってた", ["聞く", "う", "と思う", "てた"]),
    ("沈んで", ["沈む", "んで"]),
    ("死んどる", ["死ぬ", "んどる"]),
    ("馴染めないでいる", ["馴染む", "える", "ない", "でいる"]),
    ("ちょっと強引なところがあるから", ["ちょっと", "強引", "な", "ところ", "が", "ある", "から"]),
    ("また寒くなるな", ["また", "寒い", "くなる", "な"]),
    ("空を飛べる機械", ["空を飛ぶ", "える", "機械"]),
    ("だったら普通に金<wbr>貸せって言えよ", ["だったら", "普通に", "金", "貸す", "って言う", "よ"])
])
def test_misc_stuff(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("しろ", ["しろ"]),
    ("後で下に下りてらっしゃいね", ["後で", "下に", "下りる", "て", "らっしゃい", "ね"]),
])
def test_yield_to_surface(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, excluded, expected_output", [
    ("厳密に言えば　俺一人が友達だけど",
     [WordExclusion.global_("厳密に言えば"), WordExclusion.global_("言え"), WordExclusion.global_("だけど")],
     ["厳密", "に", "言う", "ば", "俺", "一人", "が", "友達", "だ", "けど"]),
    ("厳密に言えばだけど俺一人が友達だけど",
     [WordExclusion.at_index("だけど", 6)],  # You don't get to exclude tokens, it would mutilate the text, so this will remain.
     ["厳密に言えば", "だけど", "俺", "一人", "が", "友達", "だけど"]),
    ("私は毎日ジョギングをすることを習慣にしています。",
     [WordExclusion.at_index("にして", 17), WordExclusion.at_index("にし", 17), WordExclusion.at_index("して", 18), WordExclusion.at_index("し", 18), WordExclusion.at_index("してい", 18), WordExclusion.at_index("い", 12), WordExclusion.global_("にする")],
     ["私", "は", "毎日", "ジョギング", "を", "する", "こと", "を", "習慣", "に", "する", "ている", "ます"]),
    ("私は毎日ジョギングをすることを習慣にしています。",
     [WordExclusion.at_index("にして", 17), WordExclusion.at_index("にし", 17), WordExclusion.at_index("して", 18), WordExclusion.at_index("し", 18), WordExclusion.at_index("してい", 18)],
     ["私", "は", "毎日", "ジョギング", "を", "する", "こと", "を", "習慣", "にする", "ている", "ます"]),
    ("頑張れたというか", [WordExclusion.global_("頑張る"),WordExclusion.global_("頑張れ")], ["える", "た", "というか"]),
    ("いらっしゃいません", [WordExclusion.global_("いらっしゃいませ")], ["いらっしゃいます", "ん"]),
    ("風の強さに驚きました", [WordExclusion.global_("風の強い")], ["風", "の", "強さ", "に", "驚き", "ます", "た"])
])
def test_exclusions(sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, excluded, expected_output)

@pytest.mark.usefixtures("setup_collection_with_select_data")
@pytest.mark.parametrize("sentence, expected_output", [
    ("風の強さに驚きました", ["風の強い", "風", "の", "強さ", "強", "強い", "さ", "に", "驚き", "驚く", "まし:ませ", "ます", "た"])
])
def test_all_words_equal(sentence: str, expected_output: list[str]) -> None:
    assert_all_words_equal(sentence, expected_output)
