from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from fixtures.collection_factory import inject_collection_with_select_data
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from tests.language_services_tests.janome_tests.test_sentence_analysis_viewmodel_common import assert_all_words_equal, assert_display_words_equal_and_that_analysis_internal_state_is_valid

if TYPE_CHECKING:
    from collections.abc import Iterator

# noinspection PyUnusedFunction
@pytest.fixture(scope="module", autouse=True)
def setup_collection_with_select_data() -> Iterator[None]:
    with inject_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.parametrize("sentence, expected_output", [

])
def test_new_stuff(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.parametrize("sentence, expected_output", [
        ("お金貸せって", ["お金", "貸す", "え", "って"]),
        ("お前に会えて", ["お前", "に", "会う", "える", "て"]),
        ("逆に大丈夫に思えてくる", ["逆に", "大丈夫", "に", "思える", "て", "くる"]),
        ("黙れ", ["黙る", "え"]),
        ("楽しめてる", ["楽しむ", "える", "てる"]),
        ("会えたりしない", ["会う", "える", "たり", "する", "ない"]),
        ("くれよ", ["くれる", "え", "よ"]),
        ("放せよ　俺は…", ["放す", "え", "よ", "俺", "は"]),
        ("出ていけ", ["出ていく", "え"]),
        ("進めない", ["進める", "ない"]),
        ("さっさと傷を清めてこい", ["さっさと:[MISSING]", "傷", "を", "清める", "てこ", "い"]),
        ("清めの一波", ["清め", "の", "一波:[MISSING]"]),
        ("ここは清められ", ["ここ", "は", "清める", "られる"]),
        ("その物陰に隠れろ", ["その", "物陰", "に", "隠れる", "ろ"]),
        ("聞けよ", ["聞え", "よ"])
])
def test_godan_potential_and_imperative(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.parametrize("sentence, expected_output", [
        ("食べろ", ["食べる", "ろ"]),
        ("食べよ", ["食べる", "よ"]),  # rare in contemporary japanese, may well be a missspelling of 食べよう
        ("見つけよ", ["見つける", "よ"]),
        ("捕まえよ", ["捕まえる", "よ"]),
        ("離れよ", ["離れる", "よ"]),
        ("落ち着け！", ["落ち着く", "え"]),
        ("食べよう", ["食べる", "う"]),  # not an imperative, just a suggestion
])
def test_ichidan_imperative(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.parametrize("sentence, expected_output", [
        ("書きなさい", ["書く", "なさい"]),
])
def test_i_imperative_forms(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.parametrize("sentence, expected_output", [

])
def test_bugs_todo_fixme(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

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
        ("俺に謝られても", ["俺", "に", "謝る", "あれても"]),
        ("いいのかよ", ["いい", "の", "かよ"]),
        ("立ってるのかと思った", ["立つ", "てる", "のか", "と思う", "た"]),
        ("ないと思う", ["ない", "と思う"]),
        ("しても", ["する", "ても"]),
        ("見えなくなったって そんな", ["見える", "なくなる", "たって", "そんな"]),
        ("焼けたかな", ["焼ける", "た", "かな"]),
        ("何て言うか<wbr>さ", ["何", "て言うか:ていうか", "さ"]),
        ("また来ような", ["また", "来る", "う", "な"]),
        ("何なんだろうな", ["何だ", "だろう", "な"]),
        ("存在したね", ["存在", "する", "た", "ね"]),
        ("作るに決まってるだろ", ["作る", "に決まってる", "だろ"]),
        ("知らないんでしょう", ["知らない", "ん", "でしょう"]),
        ("横取りされたらたまらん", ["横取り", "される", "たら", "たまらん"]),
        ("ガチだったんでしょ", ["ガチ", "だった", "ん", "でしょ"]),
        ("どうしちゃったんだろうな", ["どう", "しちゃう", "たん:たの", "だろう", "な"]),
        ("良いものを食べる", ["良い", "もの", "を", "食べる"]),
        ("いいものを食べる", ["いい", "もの", "を", "食べる"]),
        ("うまく笑えずに", ["うまく", "笑える", "ずに"]),  # うまく disappeared when we made all verbs inflecting words by default
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
        ("だったら普通に金<wbr>貸せって言えよ", ["だったら", "普通に", "金", "貸す", "え", "って言う", "え", "よ"]),
        ("出会える", ["出会える"]),
        ("頑張れた", ["頑張る", "える", "た"]),
        ("頑張れ", ["頑張れ"]),
        ("私たちなら嘘をつかずに付き合っていけるかもしれないね", ["私たち", "なら", "嘘をつく", "ずに", "付き合う", "ていける", "かもしれない", "ね"]),
        ("どやされても知らんぞ", ["どやす", "あれる", "ても知らん:ても知らない", "ぞ"])
])
def test_misc_stuff(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

@pytest.mark.parametrize("sentence, expected_output", [
        ("しろ", ["しろ"]),
        ("後で下に下りてらっしゃいね", ["後で", "下に", "下りる", "て", "らっしゃい", "ね"]),
])
def test_yield_to_surface(sentence: str, expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, [], expected_output)

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
        ("頑張れたというか", [WordExclusion.global_("頑張る"), WordExclusion.global_("頑張れ")], ["える", "た", "というか"]),
        ("いらっしゃいません", [WordExclusion.global_("いらっしゃいませ")], ["いらっしゃいます", "ん"]),
        ("風の強さに驚きました", [WordExclusion.global_("風の強い")], ["風", "の", "強さ", "に", "驚き", "ます", "た"])
])
def test_exclusions(sentence: str, excluded: list[WordExclusion], expected_output: list[str]) -> None:
    assert_display_words_equal_and_that_analysis_internal_state_is_valid(sentence, excluded, expected_output)

@pytest.mark.parametrize("sentence, expected_output", [
        ("風の強さに驚きました", ["風の強い", "風", "の", "強さ", "強", "強い", "さ", "に", "驚き", "驚く", "まし", "ます", "た"])
])
def test_all_words_equal(sentence: str, expected_output: list[str]) -> None:
    assert_all_words_equal(sentence, expected_output)
