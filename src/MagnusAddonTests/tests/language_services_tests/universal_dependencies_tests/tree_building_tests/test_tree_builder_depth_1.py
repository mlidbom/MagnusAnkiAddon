from typing import Any

import pytest

from language_services.universal_dependencies import ud_tokenizers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers import test_runner
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

N = UDTreeNodeSpec
R = UDTreeSpec

# noinspection PyUnusedClass, PyUnusedName
pytestmark = pytest.mark.skip("This idea about separate tests for separate depths sounded good, but in the end I think it is causing more work rather than saving work.")

def only_string_params(param: Any) -> str: return param if isinstance(param, str) else ''

@pytest.mark.parametrize('sentence, tokenizer, expected', [
    ("意外とかっこいいな", None, R(N('意外と', '', ''),N('かっこいい', '', '', [N('かっこ', '', '格好'), N('いい', '', '良い')]),N('な', '', ''))),
    ("友達だから余計に気になっちゃうんだよ", None, R()),
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", None, R()),
    ("探しているんですか", None, R()),
    ("なかったかな", None, R(N('なかった', '', ''),N('かな', '', '', [N('か', '', ''), N('な', '', '')]))),
    ("離れていくよ", None, R()),
    ("よかったじゃん", None, R()),
    ("そっちへ行ったぞ", None, R()),
    ("いつまでも来ないと知らないからね", None, R()),
], ids=only_string_params)
def test_sentences(sentence: str, tokenizer: UDTokenizer, expected: R) -> None:
    run_tests(expected, tokenizer if tokenizer else ud_tokenizers.default, sentence)

@pytest.mark.parametrize('sentence, expected', [
    ("夢を見た", R(N('夢を', '', ''),N('見た', '', ''))),
    ("よかった", R()),
    ("良かった", R()),
    ("良ければ", R()),
    ("良かったら", R()),
    ("当てられても", R()),
    ("逃げたり", R()),
    ("だったら", R()),
    ("だろう", R()),
    ("するためでした", R(N('する', '', '為る'),N('ためでした', '', ''))),
    ("知らない", R()),
    ("良くない", R(N('良く', '良い', ''),N('ない', '', '無い'))),
    ("食べてもいいけど", R()),
    ("としたら", R()),
    ("行きたい所全部行こう", R(N('行きたい所', '', '', [N('行きたい', '', ''), N('所', '', '')]),N('全部', '', ''),N('行こう', '行く', ''))),
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", R()),
    ("一度夢を見た", R(N('一度', '', ''),N('夢を見た', '夢を見る', '', [N('夢を', '', ''), N('見た', '', '')]))),
    ("先生にいいように言って", R(N('先生に', '', ''),N('いいように言って', '', '', [N('いいように', '', ''), N('言って', '', '')]))),
    ("自分のことを知ってもらえてない人に", R(N('自分の', '', ''),N('ことを知ってもらえてない人に', '', '', [N('ことを', '', ''), N('知ってもらえてない', '', ''), N('人に', '', '')]))),
    ("ように言ったのも", R()),
    ("いるのにキス", R()),
    ("聞かなかったことにしてあげる", R()),
    ("とりあえず　ご飯食べよう", R()),
    ("ダメダメ私を助けて", R(N('ダメダメ', '', ''),N('私を助けて', '', '', [N('私を', '', ''), N('助けて', '', '')]))),
    ("ついに素晴らしい女性に逢えた。", R(N('ついに', '', '遂に'),N('素晴らしい女性に', '', '', [N('素晴らしい', '', ''), N('女性に', '', '')]),N('逢えた。', '', ''))),
    ("言われるまで気づかなかった", R()),
    ("一度聞いたことがある", R()),
    ("言えばよかった", R()),
], ids=only_string_params)
def test_sentences_with_no_nodes_at_this_depth(sentence: str, expected: R) -> None:
    run_tests(expected, ud_tokenizers.default, sentence)

@pytest.mark.parametrize('sentence, tokenizer, expected', [
    ("あいつが話の中に出てくるのが", ud_tokenizers.gendai, R()),
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_tokenizers.gendai, R(N('ううん', '', ''),N('藤宮さんは', '', '', [N('藤宮', 'フジミヤ', ''), N('さんは', '', '')]),N('日記を捨てるような人じゃない', '', '', [N('日記を', '', ''), N('捨てるような', '', ''), N('人じゃない', '', '')]))),
], ids=only_string_params)
def test_sentences_with_no_nodes_at_this_depth_using_alt_tokenizer(sentence: str, tokenizer: UDTokenizer, expected: R) -> None:
    run_tests(expected, tokenizer, sentence)

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str) -> None:
    test_runner.run_tests_for_level(expected, parser, sentence, 1)
