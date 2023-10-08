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


@pytest.mark.parametrize('sentence, expected', [
    ("意外とかっこいいな", R(N('意外と', '', '', [N('意外と', '', '')]),N('かっこいいな', '', '', [N('かっこいい', '', ''), N('な', '', '')]))),
    ("友達だから余計に気になっちゃうんだよ", R(N('友達だから', '', '', [N('友達だから', '', '')]),N('余計に', '', '', [N('余計に', '', '')]),N('気に', '', '', [N('気に', '', '')]),N('なっちゃうんだよ', '', '', [N('なっちゃうんだ', '', ''), N('よ', '', '')]))),
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", R(N('今じゃ', '', '', [N('今じゃ', '', '')]),N('町は', '', '', [N('町は', '', '')]),N('夜でも', '', '', [N('夜でも', '', '')]),N('明るいし', '', '', [N('明るいし', '', '')]),N('もう', '', '', [N('もう', '', '')]),N('会うこともないかもな', '', '', [N('会うこともないかも', '', ''), N('な', '', '')]))),
    ("探しているんですか", R(N('探しているんですか', '', '', [N('探しているんです', '', ''), N('か', '', '')]))),
    ("なかったかな", R(N('なかったかな', '', '', [N('なかった', '', ''), N('かな', '', '')]))),
    ("離れていくよ", R(N('離れていくよ', '', '', [N('離れていく', '', ''), N('よ', '', '')]))),
    ("よかったじゃん", R(N('よかったじゃん', '', '', [N('よかった', '', ''), N('じゃん', '', '')]))),
    ("そっちへ行ったぞ", R(N('そっちへ', '', '', [N('そっちへ', '', '')]),N('行ったぞ', '', '', [N('行った', '', ''), N('ぞ', '', '')]))),
    ("いつまでも来ないと知らないからね", R(N('いつまでも', '', '', [N('いつまでも', '', '')]),N('来ないと', '', '', [N('来ないと', '', '')]),N('知らないからね', '', '', [N('知らないから', '', ''), N('ね', '', '')]))),

], ids=only_string_params)
def test_remove_particle_phrase_final(sentence: str, expected: R) -> None:
    run_tests(expected, ud_parsers.best, sentence)


@pytest.mark.parametrize('sentence, parser, expected', [
     ("としたら", ud_parsers.gendai, R(N('としたら', '', ''))),
], ids=only_string_params)
def test_unsatisfied_dictionary_word_missing(sentence: str, parser: UDTokenizer | None, expected: R) -> None:
    run_tests_with_level_0_cloned_to_level_1(expected, parser if parser else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    # todo here we have sequential tokens with the same head, but not compounded because the head is the last token...
    ("良くない", None, R(N('良くない', '', ''))),
    #todo 行きたい所
    ("行きたい所全部行こう", None, R(N('行きたい所', '', ''),N('全部', '', ''),N('行こう', '行く', ''))),
], ids=only_string_params)
def test_unsatisfied_sequential_identical_heads_not_compounded(sentence: str, parser: UDTokenizer | None, expected: R) -> None:
    run_tests_with_level_0_cloned_to_level_1(expected, parser if parser else ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    # todo. only fetching descendents does not play well with expressions...
    #  things like 調べて here that is an andverbial clause modifier for the later よかった which is not compounded
    # BUT. This seems like an edge case. Tree building should perhaps not be complicated by trying to autodect dictionary phrases.
    # For now, maybe we'll make detecting dictionary expressions a post processing step tested separately.
    # on the other hand, we DO have the information. The previous tokens do have the later tokens as their heads
    # on the third hand, if we always fetch all heads in both directions that's always the whole string, right?
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", None, R(N('ごめん', '', '御免'), N('自分から', '', ''), N('誘っといて', '', ''), N('ちゃんと', '', ''), N('調べておけば', '', ''), N('よかった', '', ''))),
    ("夢を見た", None, R(N('夢を', '', ''), N('見た', '', ''))),
    ("一度夢を見た", None, R(N('一度', '', ''), N('夢を', '', ''), N('見た', '', ''))),
    # todo いいよう
    ("先生にいいように言って", None, R(N('先生に', '', ''),N('いいように言って', '', ''))),
    # not a disaster, but I do miss 話の中に
    ("あいつが話の中に出てくるのが", ud_parsers.gendai, R(N('あいつが', '', ''),N('話の', '', ''),N('中に', '', ''),N('出てくるのが', '', ''))),
    # not a disaster, but I want 藤宮さん compounded
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai, R(N('ううん', '', ''),N('藤宮さんは', '', ''),N('日記を', '', ''),N('捨てるような', '', ''),N('人じゃない', '', ''))),
    # 自分のこと
    ("自分のことを知ってもらえてない人に", None, R(N('自分の', '', ''),N('ことを', '', ''),N('知ってもらえてない', '', ''),N('人に', '', ''))),
    # ように言った
    ("ように言ったのも", None, R(N('ように', '', ''), N('言ったのも', '', ''))),
])
def test_unsatisfied_dictionary_expression_missing(sentence: str, parser: UDTokenizer | None, expected: R) -> None:
    run_tests_with_level_0_cloned_to_level_1(expected, parser if parser else ud_parsers.best, sentence)

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

    # todo ても, てもいい (も,いい: fixed_multiword_expression, て-head)
    ("食べてもいいけど", R(N('食べてもいいけど', '', ''))),
    # todo (いる)のに(marker,case_marking: いる-head)
    ("いるのにキス", R(N('いるのに', '', ''), N('キス', '', ''))),
    # todo (聞か)なかった:ことにし(-て) (なかっ:auxiliary, た:auxiliary, こと:compound  聞か-head) (に,し fixed_multiword こと-head)
    ("聞かなかったことにしてあげる", R(N('聞かなかったことにして', '', ''), N('あげる', '', '上げる'))),
    # todo volitional form..
    ("とりあえず　ご飯食べよう", R(N('とりあえず', '', '取り敢えず'), N('ご飯', '', '御飯'), N('食べよう', '食べる', ''))),
], ids=only_string_params)
def test_sentences_we_are_unsatisfied_with(sentence: str, expected: R) -> None:
    run_tests_with_level_0_cloned_to_level_1(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, expected', [
    ("ダメダメ私を助けて", R(N('ダメダメ', '', ''), N('私を', '', ''), N('助けて', '', ''))),
    ("知らない", R(N('知らない', '', ''))),
    ("ついに素晴らしい女性に逢えた。", R(N('ついに', '', '遂に'), N('素晴らしい', '', ''), N('女性に', '', ''), N('逢えた。', '', ''))),
    ("するためでした", R(N('するためでした', '', ''))),
    ("言われるまで気づかなかった", R(N('言われるまで', '', ''), N('気づかなかった', '', ''))),
    ("当てられても", R(N('当てられても', '', ''))),
    ("逃げたり", R(N('逃げたり', '', ''))),
    ("一度聞いたことがある", R(N('一度', '', ''), N('聞いたことがある', '', ''))),
    ("よかった", R(N('よかった', '', ''))),
    ("良かった", R(N('良かった', '', ''))),
    ("良ければ", R(N('良ければ', '', ''))),
    ("良かったら", R(N('良かったら', '', ''))),
    ("言えばよかった", R(N('言えば', '', ''), N('よかった', '', ''))),
    ("だったら", R(N('だったら', '', ''))),
    ("だろう", R(N('だろう', '', ''))),

], ids=only_string_params)
def test_sentences_the_best_parser_does_well(sentence: str, expected: R) -> None:
    run_tests_with_level_0_cloned_to_level_1(expected, ud_parsers.best, sentence)

def run_tests(expected: UDTreeSpec, parser: UDTokenizer, sentence: str) -> None:
    test_runner.run_tests(expected, parser, sentence, 1)

def run_tests_with_level_0_cloned_to_level_1(expected: UDTreeSpec, parser: UDTokenizer, sentence: str) -> None:
    test_runner.run_tests(expected.clone_level_0_to_level_1(), parser, sentence, 1)

