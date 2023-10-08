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

@pytest.mark.parametrize('sentence, parser, expected', [
    ("意外とかっこいいな", None, R(N('意外と', '', ''), N('かっこいい', '', ''), N('な', '', ''))),
], ids=only_string_params)
def test_unsatisfied_dictionary_word_missing(sentence: str, parser: UDTokenizer | None, expected: R) -> None:
    run_tests(expected, parser if parser else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    ("行きたい所全部行こう", None, R()),
], ids=only_string_params)
def test_unsatisfied_sequential_identical_heads_not_compounded(sentence: str, parser: UDTokenizer | None, expected: R) -> None:
    run_tests(expected, parser if parser else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    # todo. only fetching descendents does not play well with expressions...
    #  things like 調べて here that is an andverbial clause modifier for the later よかった which is not compounded
    # BUT. This seems like an edge case. Tree building should perhaps not be complicated by trying to autodect dictionary phrases.
    # For now, maybe we'll make detecting dictionary expressions a post processing step tested separately.
    # on the other hand, we DO have the information. The previous tokens do have the later tokens as their heads
    # on the third hand, if we always fetch all heads in both directions that's always the whole string, right?
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", None, R(N('ごめん', '', '御免'), N('自分から', '', ''), N('誘っといて', '', ''), N('ちゃんと', '', ''), N('調べておけば', '', ''), N('よかった', '', ''))),
    ("友達だから余計に気になっちゃうんだよ", None, R(N('友達だから', '', ''), N('余計に', '', ''), N('気に', '', ''), N('なっちゃうんだ', '', ''), N('よ', '', ''))),
    # todo いいよう
    ("先生にいいように言って", None, R(N('先生に', '', ''), N('いいように言って', '', ''))),
    # not a disaster, but I do miss 話の中に
    ("あいつが話の中に出てくるのが", ud_parsers.gendai, R(N('あいつが', '', ''), N('話の', '', ''), N('中に', '', ''), N('出てくるのが', '', ''))),
    # 自分のこと
    ("自分のことを知ってもらえてない人に", None, R(N('自分の', '', ''), N('ことを知ってもらえてない人に', '', ''))),
    # ように言った
    ("ように言ったのも", None, R(N('ように', '', ''), N('言ったのも', '', ''))),
], ids=only_string_params)
def test_unsatisfied_dictionary_expression_missing(sentence: str, parser: UDTokenizer | None, expected: R) -> None:
    run_tests(expected, parser if parser else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, expected', [
    # todo: maybe use dictionary lookup for sequencial tokens with the same head to look for compounds?
    # maybe the deprel and/or pos will tell us what to merge most times?
    # sequential items with the same head(usually previous) are interesting.
    # do they also need other attributes to me "mergeable"?
    # deprels of interest
    # fixed_multiword_expression seems a no-brainer, these go together with each other if sequential. How do they relate to their head?
    # compound should be compounded  with head? 会う(こと:compound)
    #   even when coming before head! (かっこ:compound, head:いい(いい:root))
    # then fixed-multiword attaches to compound? to form a larger continuation:
    #  (聞か(なかっ:aux/infl|た:aux/infl|こと:compound/noun(に:multi/case|し:multi/verb_bound)))) then as we recurse we want to first drop the 聞か, then the こと
    #

    # todo (夜)でも(case marking, 夜-head), かも(marker/case_marking, 会う-head)
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", R(N('今じゃ', '', ''),N('町は', '', ''),N('夜でも', '', ''),N('明るいし', '', ''),N('もう会うこともないかも', '', ''),N('な', '', ''))),
    # todo ても, てもいい (も,いい: fixed_multiword_expression, て-head)

    # todo (いる)のに(marker,case_marking: いる-head)
    ("いるのにキス", R(N('いるのに', '', ''), N('キス', '', ''))),
    # todo (聞か)なかった:ことにし(-て) (なかっ:auxiliary, た:auxiliary, こと:compound  聞か-head) (に,し fixed_multiword こと-head)
    ("聞かなかったことにしてあげる", R(N('聞かなかったことにして', '', ''), N('あげる', '', '上げる'))),
    # todo volitional form..
    ("とりあえず　ご飯食べよう", R()),
], ids=only_string_params)
def test_sentences_we_are_unsatisfied_with(sentence: str, expected: R) -> None:
    run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, tokenizer, expected', [
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai, R(N('ううん藤宮さんは', '', ''),N('日記を捨てるような人じゃない', '', ''))),
], ids=only_string_params)
def test_sentences_alternative_tokenizer_does_better(sentence: str, tokenizer: UDTokenizer, expected: R) -> None:
    run_tests(expected, tokenizer, sentence)

@pytest.mark.parametrize('sentence, expected', [
    ("ダメダメ私を助けて", R()),
    ("一度夢を見た", R()),
    ("いつまでも来ないと知らないからね", R(N('いつまでも', '', ''), N('来ないと', '', ''), N('知らないから', '', ''), N('ね', '', ''))),
    ("ついに素晴らしい女性に逢えた。", R(N('ついに', '', '遂に'), N('素晴らしい女性に', '', ''), N('逢えた。', '', ''))),
    ("言われるまで気づかなかった", R(N('言われるまで', '', ''), N('気づかなかった', '', ''))),
    ("一度聞いたことがある", R()),
    ("言えばよかった", R(N('言えば', '', ''), N('よかった', '', ''))),
    ("そっちへ行ったぞ", R(N('そっちへ', '', ''), N('行った', '', ''), N('ぞ', '', ''))),
], ids=only_string_params)
def test_sentences_the_best_parser_does_well(sentence: str, expected: R) -> None:
    run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, expected', [
    ("夢を見た", R()),
    ("としたら", R()),
    ("良くない", R()),
    ("食べてもいいけど", R()),
    ("知らない", R()),
    ("するためでした", R()),
    ("なかったかな", R(N('なかった', '', ''),N('かな', '', ''))),
    ("離れていくよ", R(N('離れていく', '', ''),N('よ', '', ''))),
    ("よかったじゃん", R(N('よかった', '', ''), N('じゃん', '', ''))),
    ("探しているんですか", R(N('探しているんです', '', ''),N('か', '', ''))),
    ("よかった", R()),
    ("良かった", R()),
    ("良ければ", R()),
    ("良かったら", R()),
    ("だったら", R()),
    ("だろう", R()),
    ("当てられても", R()),
    ("逃げたり", R()),
], ids=only_string_params)
def test_sentences_with_no_nodes_at_this_depth(sentence: str, expected: R) -> None:
    run_tests(expected, ud_parsers.best, sentence)

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str) -> None:
    test_runner.run_tests_for_level(expected, parser, sentence, 0)
