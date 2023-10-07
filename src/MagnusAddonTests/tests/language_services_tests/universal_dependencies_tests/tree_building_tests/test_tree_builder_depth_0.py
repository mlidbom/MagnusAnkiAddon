from typing import Any

import pytest

from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from sysutils.ex_str import full_width_space
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_node_spec import UDTreeNodeSpec
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.helpers.ud_tree_spec import UDTreeSpec

N = UDTreeNodeSpec
R = UDTreeSpec

def only_string_params(param:Any) -> str: return param if isinstance(param, str) else ''

@pytest.mark.parametrize('sentence, expected', [
    #todo: maybe use dictionary lookup for sequencial tokens with the same head to look for compounds?
    #maybe the deprel and/or pos will tell us what to merge most times?
    #sequential items with the same head(usually previous) are interesting.
    #do they also need other attributes to me "mergeable"?
    #deprels of interest
    # fixed_multiword_expression seems a no-brainer, these go together with each other if sequential. How do they relate to their head?
    # compound should be compounded  with head? 会う(こと:compound)
    # then fixed-multiword attaches to compound? to form a larger continuation:
    #  (聞か(なかっ:aux/infl|た:aux/infl|こと:compound/noun(に:multi/case|し:multi/verb_bound)))) then as we recurse we want to first drop the 聞か, then the こと
    #
    #todo (夜)でも(case marking, 夜-head), かも(marker/case_marking, 会う-head)
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", R(N('今じゃ町は', '', ''),N('夜でも明るいし', '', ''),N('もう会うこと', '', ''),N('もないかもな', '', ''))),
    #todo ても, てもいい (も,いい: fixed_multiword_expression, て-head)
    ("食べてもいいけど", R(N('食べてもいいけど', '', ''))),
    #todo (いる)のに(marker,case_marking: いる-head)
    ("いるのにキス", R(N('いるのにキス', '', ''))),
    #todo (聞か)なかった:ことにし(-て) (なかっ:auxiliary, た:auxiliary, こと:compound  聞か-head) (に,し fixed_multiword こと-head)
    ("聞かなかったことにしてあげる", R(N('聞かなかったことにしてあげる', '', ''))),
    #todo volitional form..
    ("とりあえず　ご飯食べよう", R(N('とりあえずご飯食べよう', '', ''))),
    #todo いいよう
    ("先生にいいように言って", R(N('先生にいいように言って', '', ''))),
    #todo: かっこいい
    ("意外とかっこいいな", R(N('意外とかっこいいな', '', ''))),
   ], ids=only_string_params)
def test_sentences_we_are_unsatisfied_with(sentence: str, expected: R) -> None: run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, expected', [
    ("ように言ったのも", R(N('ように言ったのも', '', ''))),
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", R(N('ごめん自分から誘っといてちゃんと調べて', '', ''),N('おけばよかった', '', ''))),
    ("探しているんですか", R(N('探しているんですか', '', ''))),
    ("ダメダメ私を助けて", R(N('ダメダメ私を助けて', '', ''))),
    ("知らない", R(N('知らない', '', ''))),
    ("いつまでも来ないと知らないからね", R(N('いつまでも来ないと', '', ''),N('知らないからね', '', ''))),
    ("ついに素晴らしい女性に逢えた。", R(N('ついに素晴らしい女性に逢えた。', '', ''))),
    ("なかったかな", R(N('なかったかな', '', ''))),
    ("離れていくよ", R(N('離れていくよ', '', ''))),
    ("夢を見た", R(N('夢を見た', '夢を見る', ''))),
    ("言われるまで気づかなかった", R(N('言われるまで気づかなかった', '', ''))),
    ("行きたい所全部行こう", R(N('行きたい所', '', ''),N('全部行こう', '', ''))),
    ("当てられても", R(N('当てられても', '', ''))),
    ("逃げたり", R(N('逃げたり', '', ''))),
    ("するためでした", R(N('するためでした', '', ''))),
    ("一度聞いたことがある", R(N('一度聞いたこと', '', ''),N('がある', '', ''))),
    ("友達だから余計に気になっちゃうんだよ", R(N('友達だから余計に気になっちゃうん', '', ''),N('だよ', '', ''))),
    ("自分のことを知ってもらえてない人に", R(N('自分のことを', '', ''),N('知ってもらえてない人に', '', ''))),
    ("よかった", R(N('よかった', '', ''))),
    ("良かった", R(N('良かった', '', ''))),
    ("良くない", R(N('良くない', '', ''))),
    ("良ければ", R(N('良ければ', '', ''))),
    ("良かったら", R(N('良かったら', '', ''))),
    ("よかったじゃん", R(N('よかったじゃん', '', ''))),
    ("言えばよかった", R(N('言えばよかった', '', ''))),
    ("一度夢を見た", R(N('一度夢を見た', '', ''))),
    ("そっちへ行ったぞ", R(N('そっちへ行ったぞ', '', ''))),
    ("だったら", R(N('だったら', '', ''))),
    ("だろう", R(N('だろう', '', ''))),


   ], ids=only_string_params)
def test_sentences_the_best_parser_does_well(sentence: str, expected: R) -> None: run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai, R(N('ううん藤宮さんは', '', ''),N('日記を捨てるような', '', ''),N('人じゃない', '', ''))),
    ("としたら", ud_parsers.gendai, R(N('としたら', '', ''))),
    ("あいつが話の中に出てくるのが", ud_parsers.gendai, R(N('あいつが話の中に出てくるのが', '', ''))),

], ids=only_string_params)
def test_sentences_done_better_by_alternative_parser(sentence: str, parser: UDTokenizer, expected: R) -> None: run_tests(expected, parser, sentence)

# @pytest.mark.parametrize('sentence, parser, expected', [
#     ("カバンに入れっぱなしだった", ud_parsers.best, R())
# ], ids=only_string_params)
# def test_temp(sentence: str, parser: UDParser, expected: UDTextTree) -> None: run_tests(expected, parser, sentence)


def run_tests(expected:R, parser: UDTokenizer, sentence:str) -> None:
    print()
    parser = parser if parser else ud_parsers.best
    real_result = ud_tree_builder.build_tree(parser, sentence, collapse_identical_levels=False)
    spec_result = R.from_ud_tree(real_result, max_depth=0)
    print(f"{parser.name} : {sentence}")
    print(parser.parse(sentence).to_tree())
    print()
    print(f"str: {sentence}")
    print(str(spec_result))
    print("expected-repr:")
    print(repr(expected))
    print("repr:")
    print(repr(spec_result))
    print("repr-single-line:")
    print(repr(spec_result).replace("\n", '').replace(full_width_space, ''))

    assert spec_result == expected






@pytest.mark.parametrize("sentence", [
    #"朝、近所をぶらぶらした",
    # "そんなに気になるなら あの時俺も友達だって言えばよかったじゃん",
    # "普段どうやって日記読んでたんだ",
    # "何か意味があるんだと思う",
    # "いつまでも来ないと知らないからね",
    # "離れていくよ",
    # "ああだからあの時忘れんなって言ったのに",
    # "ダメダメ私を助けて",
    # "ついに素晴らしい女性に逢えた。",
    # "ううん藤宮さんは日記を捨てるような人じゃない",
    # "探しているんですか",
    #"行きたい所全部行こう",
    #"当てられても",
    # "一度聞いたことがある",
    # "よかったじゃん",
    # "言えばよかった",
    # "言われるまで気づかなかった",
    # "夢を見た",
    # "知らない",
    # "何よあの態度偉そうに",
    # "これから本題に入るんだけど",
    # "食べられるもの",
    # "俺以外に友達がいなくてよかったとか　絶対思っちゃダメなのに",
    # "日代さんが 先生に知らせてくれたらしい",
    # "やっぱりあの噂ホントだったんだ",
    # "だったら記憶喪失の振りすることも簡単だよな",
    # "だったら記憶喪失の振りすることも簡単だよな"¨
    #"食べてもいいけど",
    #"ケータイ持ってるやつは自宅に連絡しておけ",
    #"なぜかというと",
    #"あり得るか",
    #"二千九百円",
    #"じゃ　神経衰弱をやろう",
    #"この前の　放課後"
    #"と…とりあえず　ご飯食べよう"
    "意外とかっこいいな"
])
def test_compare_parsers(sentence: str) -> None:
    print()
    print(sentence)
    for parser in ud_parsers.all_parsers:
        print(f"{parser.name} : {sentence}")
        print(parser.parse(sentence).to_tree())
        print()

    for parser in ud_parsers.all_parsers:
        print(f"{parser.name} : {sentence}")
        print(ud_tree_builder.build_tree(parser, sentence))
        print()
