from typing import Any

import pytest

from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers import test_runner
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

N = UDTreeNodeSpec
R = UDTreeSpec

def only_string_params(param: Any) -> str: return param if isinstance(param, str) else ''


@pytest.mark.parametrize('sentence, tokenizer, expected', [
    ("意外とかっこいいな", None, R(N('意外と', '', ''),N('かっこいいな', '', '', [N('かっこいい', '', ''), N('な', '', '')]))),
    ("友達だから余計に気になっちゃうんだよ", None, R(N('友達だから', '', ''),N('余計に', '', ''),N('気に', '', ''),N('なっちゃうんだよ', '', '', [N('なっちゃうんだ', '', ''), N('よ', '', '')]))),
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", None, R(N('今じゃ', '', ''),N('町は', '', ''),N('夜でも', '', ''),N('明るいし', '', ''),N('もう', '', ''),N('会うこともないかもな', '', '', [N('会うこともないかも', '', ''), N('な', '', '')]))),
    ("探しているんですか", None, R(N('探しているんです', '', ''),N('か', '', ''))),
    ("なかったかな", None, R(N('なかった', '', ''),N('かな', '', ''))),
    ("離れていくよ", None, R(N('離れていく', '', ''),N('よ', '', ''))),
    ("よかったじゃん", None, R(N('よかった', '', ''),N('じゃん', '', ''))),
    ("そっちへ行ったぞ", None, R(N('そっちへ', '', ''),N('行ったぞ', '', '', [N('行った', '', ''), N('ぞ', '', '')]))),
    ("いつまでも来ないと知らないからね", None, R(N('いつまでも', '', ''),N('来ないと', '', ''),N('知らないからね', '', '', [N('知らないから', '', ''), N('ね', '', '')]))),
    ("行きたい所全部行こう", None, R(N('行きたい所', '', ''),N('全部', '', ''),N('行こう', '行く', ''))),
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", None, R(N('ごめん', '', '御免'), N('自分から', '', ''), N('誘っといて', '', ''), N('ちゃんと', '', ''), N('調べておけば', '', ''), N('よかった', '', ''))),
    ("夢を見た", None, R(N('夢を', '', ''), N('見た', '', ''))),
    ("一度夢を見た", None, R(N('一度', '', ''), N('夢を', '', ''), N('見た', '', ''))),
    ("先生にいいように言って", None, R(N('先生に', '', ''),N('いいように言って', '', ''))),
    ("あいつが話の中に出てくるのが", ud_parsers.gendai, R(N('あいつが', '', ''),N('話の', '', ''),N('中に', '', ''),N('出てくるのが', '', ''))),
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai, R(N('ううん', '', ''),N('藤宮さんは', '', ''),N('日記を', '', ''),N('捨てるような', '', ''),N('人じゃない', '', ''))),
    ("自分のことを知ってもらえてない人に", None, R(N('自分の', '', ''),N('ことを', '', ''),N('知ってもらえてない', '', ''),N('人に', '', ''))),
    ("ように言ったのも", None, R(N('ように', '', ''), N('言ったのも', '', ''))),
    ("いるのにキス", None, R(N('いるのに', '', ''), N('キス', '', ''))),
    ("聞かなかったことにしてあげる", None, R(N('聞かなかったことにして', '', ''), N('あげる', '', '上げる'))),
    ("とりあえず　ご飯食べよう", None, R(N('とりあえず', '', '取り敢えず'), N('ご飯', '', '御飯'), N('食べよう', '食べる', ''))),
    ("ダメダメ私を助けて", None, R(N('ダメダメ', '', ''), N('私を', '', ''), N('助けて', '', ''))),
    ("ついに素晴らしい女性に逢えた。", None, R(N('ついに', '', '遂に'), N('素晴らしい', '', ''), N('女性に', '', ''), N('逢えた。', '', ''))),
    ("言われるまで気づかなかった", None, R(N('言われるまで', '', ''), N('気づかなかった', '', ''))),
    ("一度聞いたことがある", None, R(N('一度', '', ''), N('聞いたことがある', '', ''))),
    ("言えばよかった", None, R(N('言えば', '', ''), N('よかった', '', ''))),

], ids=only_string_params)
def test_sentences(sentence: str, tokenizer: UDTokenizer, expected: R) -> None:
    run_tests(expected, tokenizer if tokenizer else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence', [
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
], ids=only_string_params)
def test_sentences_swallowed_whole_at_this_level(sentence: str) -> None:
    run_tests(R(), ud_parsers.best, sentence)

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str) -> None:
    test_runner.run_tests(expected, parser, sentence, 1)
