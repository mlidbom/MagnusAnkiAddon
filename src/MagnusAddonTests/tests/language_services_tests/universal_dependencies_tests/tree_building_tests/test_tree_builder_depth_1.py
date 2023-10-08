from typing import Any

import pytest

from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers import test_runner
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.test_runner import assert_no_nodes_at_level, run_tests_for_level
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

N = UDTreeNodeSpec
R = UDTreeSpec

def only_string_params(param: Any) -> str: return param if isinstance(param, str) else ''

@pytest.mark.parametrize('sentence, tokenizer, expected', [
    ("意外とかっこいいな", None, R(N('意外と', '', ''), N('かっこいいな', '', '', [N('かっこいい', '', ''), N('な', '', '')]))),
    ("友達だから余計に気になっちゃうんだよ", None, R(N('友達だから', '', ''), N('余計に', '', ''), N('気に', '', ''), N('なっちゃうんだよ', '', '', [N('なっちゃうんだ', '', ''), N('よ', '', '')]))),
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", None, R(N('今じゃ', '', ''), N('町は', '', ''), N('夜でも', '', ''), N('明るいし', '', ''), N('もう', '', ''), N('会うこともないかもな', '', '', [N('会うこともないかも', '', ''), N('な', '', '')]))),
    ("探しているんですか", None, R(N('探しているんです', '', ''), N('か', '', ''))),
    ("なかったかな", None, R(N('なかった', '', ''), N('かな', '', ''))),
    ("離れていくよ", None, R(N('離れていく', '', ''), N('よ', '', ''))),
    ("よかったじゃん", None, R(N('よかった', '', ''), N('じゃん', '', ''))),
    ("そっちへ行ったぞ", None, R(N('そっちへ', '', ''), N('行ったぞ', '', '', [N('行った', '', ''), N('ぞ', '', '')]))),
    ("いつまでも来ないと知らないからね", None, R(N('いつまでも', '', ''), N('来ないと', '', ''), N('知らないからね', '', '', [N('知らないから', '', ''), N('ね', '', '')]))),
], ids=only_string_params)
def test_sentences(sentence: str, tokenizer: UDTokenizer, expected: R) -> None:
    run_tests(expected, tokenizer if tokenizer else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence', [
    "夢を見た",
    "よかった",
    "良かった",
    "良ければ",
    "良かったら",
    "当てられても",
    "逃げたり",
    "だったら",
    "だろう",
    "するためでした",
    "知らない",
    "良くない",
    "食べてもいいけど",
    "としたら",
    "行きたい所全部行こう",
    "ごめん　自分から誘っといて ちゃんと調べておけばよかった",
    "一度夢を見た",
    "先生にいいように言って",
    "自分のことを知ってもらえてない人に",
    "ように言ったのも",
    "いるのにキス",
    "聞かなかったことにしてあげる",
    "とりあえず　ご飯食べよう",
    "ダメダメ私を助けて",
    "ついに素晴らしい女性に逢えた。",
    "言われるまで気づかなかった",
    "一度聞いたことがある",
    "言えばよかった",
], ids=only_string_params)
def test_sentences_with_no_nodes_at_this_depth(sentence: str) -> None:
    assert_no_nodes_at_level(ud_parsers.best, sentence, 1)

@pytest.mark.parametrize('sentence, tokenizer', [
    ("あいつが話の中に出てくるのが", ud_parsers.gendai),
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai),
], ids=only_string_params)
def test_sentences_with_no_nodes_at_this_depth_using_alt_tokenizer(sentence: str, tokenizer: UDTokenizer) -> None:
    assert_no_nodes_at_level(tokenizer, sentence, 1)

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str) -> None:
    test_runner.run_tests_for_level(expected, parser, sentence, 1)
