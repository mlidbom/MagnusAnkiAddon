from typing import Any

import pytest

from language_services.universal_dependencies import ud_parsers
from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tree_building import ud_tree_builder
from sysutils.ex_str import full_width_space
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.ud_tree_node_spec import UDTreeNodeSpec
from tests.language_services_tests.universal_dependencies_tests.tree_building_tests.ud_tree_spec import UDTreeSpec

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
    # then fixed-multiword attaches to compound? to form a larger contiuation:
    #  (聞か(なかっ:aux/infl|た:aux/infl|こと:compound/noun(に:multi/case|し:multi/verb_bound)))) then as we recurse we want to first drop the 聞か, then the こと
    #
    #todo (夜)でも(case marking, 夜-head), かも(marker/case_marking, 会う-head)
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", R(N('今じゃ町は', '', '', [N('今じゃ', '', '', [N('今', '', ''), N('じゃ', '', 'で')]), N('町は', '', '', [N('町', '', ''), N('は', '', '')])]),N('夜でも明るいし', '', '', [N('夜でも', '', '', [N('夜', '', ''), N('で', '', ''), N('も', '', '')]), N('明るいし', '', '', [N('明るい', '', ''), N('し', '', '')])]),N('もう会うこと', '', '', [N('もう', '', ''), N('会うこと', '', '', [N('会う', '', ''), N('こと', '', '')])]),N('もないかもな', '', '', [N('も', '', ''), N('ない', '', '無い'), N('か', '', ''), N('も', '', ''), N('な', '', '')]))),
    #todo ても, てもいい (も,いい: fixed_multiword_expression, て-head)
    ("食べてもいいけど", R(N('食べて', '', '', [N('食べ', '食べる', ''), N('て', '', '')]),N('も', '', ''),N('いい', '', '良い'),N('けど', '', 'けれど'))),
    #todo (いる)のに(marker,case_marking: いる-head)
    ("いるのにキス", R(N('いるのに', '', '', [N('いる', '', '居る'), N('の', '', ''), N('に', '', '')]), N('キス', '', ''))),
    #todo (聞か)なかった:ことにし(-て) (なかっ:auxiliary, た:auxiliary, こと:compound  聞か-head) (に,し fixed_multiword こと-head)
    ("聞かなかったことにしてあげる", R(N('聞かなかったこと', '', '', [N('聞か', '聞く', ''), N('なかっ', 'ない', ''), N('た', '', ''), N('こと', '', '')]),N('に', '', ''),N('し', 'する', '為る'),N('て', '', ''),N('あげる', '', '上げる'))),
    #todo volitional form..
    ("とりあえず　ご飯食べよう", R(N('とりあえず', '', '取り敢えず'),N('ご飯食べよう', '', '', [N('ご飯', '', '御飯'), N('食べよう', '食べる', '')]))),
    #todo いいよう
    ("先生にいいように言って", R(N('先生に', '', '', [N('先生', '', ''), N('に', '', '')]),N('いいように言って', '', '', [N('いいように', '', '', [N('いい', '', '良い'), N('よう', '', ''), N('に', '', '')]), N('言って', '', '', [N('言っ', '言う', ''), N('て', '', '')])]))),
    #todo: かっこいい
    ("意外とかっこいいな", R(N('意外と', '', '', [N('意外', '', ''), N('と', '', '')]),N('かっこいいな', '', '', [N('かっこ', '', '格好'), N('いいな', '', '', [N('いい', '', '良い'), N('な', '', '')])]))),
   ], ids=only_string_params)
def test_sentences_we_are_unsatisfied_with(sentence: str, expected: R) -> None: run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, expected', [
    ("ように言ったのも", R(N('ように', '', '', [N('よう', '', ''), N('に', '', '')]),N('言ったのも', '', '', [N('言っ', '言う', ''), N('た', '', ''), N('の', '', ''), N('も', '', '')]))),
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", R(N('ごめん自分から誘っといてちゃんと調べて', '', '', [N('ごめん', '', '御免'), N('自分から誘っといて', '', '', [N('自分から', '', '', [N('自分', '', ''), N('から', '', '')]), N('誘っといて', '', '', [N('誘っ', '誘う', ''), N('とい', 'とく', ''), N('て', '', '')])]), N('ちゃんと調べて', '', '', [N('ちゃんと', '', ''), N('調べて', '', '', [N('調べ', '調べる', ''), N('て', '', '')])])]),N('おけばよかった', '', '', [N('おけ', 'おく', ''), N('ば', '', ''), N('よかった', '', '', [N('よかっ', 'よい', '良い'), N('た', '', '')])]))),
    ("探しているんですか", R(N('探して', '', '', [N('探し', '探す', ''), N('て', '', '')]),N('いる', '', '居る'),N('んです', '', '', [N('ん', '', 'の'), N('です', '', '')]),N('か', '', ''))),
    ("ダメダメ私を助けて", R(N('ダメダメ', '', ''), N('私を助けて', '', '', [N('私を', '', '', [N('私', '', ''), N('を', '', '')]), N('助けて', '', '', [N('助け', '助ける', ''), N('て', '', '')])]))),
    ("知らない", R(N('知らない', '', '', [N('知ら', '知る', ''), N('ない', '', '')]))),
    ("いつまでも来ないと知らないからね", R(N('いつまでも来ないと', '', '', [N('いつまでも', '', '', [N('いつ', '', ''), N('まで', '', ''), N('も', '', '')]), N('来ないと', '', '', [N('来', '来る', ''), N('ない', '', ''), N('と', '', '')])]), N('知らないからね', '', '', [N('知ら', '知る', ''), N('ない', '', ''), N('から', '', ''), N('ね', '', '')]))),
    ("ついに素晴らしい女性に逢えた。", R(N('ついに', '', '遂に'),N('素晴らしい女性に', '', '', [N('素晴らしい', '', ''), N('女性に', '', '', [N('女性', '', ''), N('に', '', '')])]),N('逢えた。', '', '', [N('逢え', '逢える', '会う'), N('た', '', ''), N('。', '', '')]))),
    ("なかったかな", R(N('なかったかな', '', '', [N('なかっ', 'ない', '無い'), N('た', '', ''), N('か', '', ''), N('な', '', '')]))),
    ("離れていくよ", R(N('離れて', '', '', [N('離れ', '離れる', ''), N('て', '', '')]), N('いく', '', '行く'), N('よ', '', ''))),
    ("夢を見た", R(N('夢を', '', '', [N('夢', '', ''), N('を', '', '')]), N('見た', '', '', [N('見', '見る', ''), N('た', '', '')]))),
    ("言われるまで気づかなかった", R(N('言われるまで', '', '', [N('言わ', '言う', ''), N('れる', '', ''), N('まで', '', '')]),N('気づかなかった', '', '', [N('気づか', '気づく', '気付く'), N('なかっ', 'ない', ''), N('た', '', '')]))),
    ("行きたい所全部行こう", R(N('行きたい所', '', '', [N('行きたい', '', '', [N('行き', '行く', ''), N('たい', '', '')]), N('所', '', '')]),N('全部行こう', '', '', [N('全部', '', ''), N('行こう', '行く', '')]))),
    ("当てられても", R(N('当てられても', '', '', [N('当て', '当てる', ''), N('られ', 'られる', ''), N('て', '', ''), N('も', '', '')]))),
    ("逃げたり", R(N('逃げたり', '', '', [N('逃げ', '逃げる', ''), N('たり', '', '')]))),
    ("するためでした", R(N('するためでした', '', '', [N('する', '', '為る'), N('ためでした', '', '', [N('ため', '', '為'), N('でし', 'です', ''), N('た', '', '')])]))),
    ("一度聞いたことがある", R(N('一度聞いたこと', '', '', [N('一度', '', ''), N('聞いたこと', '', '', [N('聞い', '聞く', ''), N('た', '', ''), N('こと', '', '')])]),N('がある', '', '', [N('が', '', ''), N('ある', '', '有る')]))),
    ("友達だから余計に気になっちゃうんだよ", R(N('友達だから余計に気になっちゃうん', '', '', [N('友達だから', '', '', [N('友達', '', ''), N('だ', '', ''), N('から', '', '')]), N('余計に', '', '', [N('余計', '', ''), N('に', '', '')]), N('気になっちゃうん', '', '', [N('気に', '', '', [N('気', '', ''), N('に', '', '')]), N('なっちゃうん', '', '', [N('なっ', 'なる', '成る'), N('ちゃう', '', ''), N('ん', '', 'の')])])]),N('だよ', '', '', [N('だ', '', ''), N('よ', '', '')]))),
    ("自分のことを知ってもらえてない人に", R(N('自分のことを', '', '', [N('自分の', '', '', [N('自分', '', ''), N('の', '', '')]), N('ことを', '', '', [N('こと', '', ''), N('を', '', '')])]),N('知ってもらえてない人に', '', '', [N('知って', '', '', [N('知っ', '知る', ''), N('て', '', '')]), N('もらえ', 'もらえる', '貰う'), N('て', 'てる', ''), N('ない', '', ''), N('人に', '', '', [N('人', '', ''), N('に', '', '')])]))),
    ("よかった", R(N('よかった', '', '', [N('よかっ', 'よい', '良い'), N('た', '', '')]))),
    ("良かった", R(N('良かった', '', '', [N('良かっ', '良い', ''), N('た', '', '')]))),
    ("良くない", R(N('良くない', '', '', [N('良く', '良い', ''), N('ない', '', '無い')]))),
    ("良ければ", R(N('良ければ', '', '', [N('良けれ', '良い', ''), N('ば', '', '')]))),
    ("良かったら", R(N('良かったら', '', '', [N('良かっ', '良い', ''), N('たら', '', '')]))),
    ("よかったじゃん", R(N('よかったじゃん', '', '', [N('よかっ', 'よい', '良い'), N('た', '', ''), N('じゃん', '', '')]))),
    ("言えばよかった", R(N('言えば', '', '', [N('言え', '言う', ''), N('ば', '', '')]),N('よかった', '', '', [N('よかっ', 'よい', '良い'), N('た', '', '')]))),
    ("一度夢を見た", R(N('一度', '', ''), N('夢を見た', '夢を見る', '', [N('夢を', '', '', [N('夢', '', ''), N('を', '', '')]), N('見た', '', '', [N('見', '見る', ''), N('た', '', '')])]))),
    ("そっちへ行ったぞ", R(N('そっちへ', '', '', [N('そっち', '', '其方'), N('へ', '', '')]),N('行ったぞ', '', '', [N('行っ', '行く', ''), N('た', '', ''), N('ぞ', '', '')]))),
    ("だったら", R(N('だったら', '', '', [N('だっ', 'だ', ''), N('たら', '', '')]))),
    ("だろう", R(N('だろう', '', ''))),


   ], ids=only_string_params)
def test_sentences_the_best_parser_does_well(sentence: str, expected: R) -> None: run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai, R(N('ううん藤宮さんは', '', '', [N('ううん', '', ''), N('藤宮さんは', '', '', [N('藤宮', 'フジミヤ', ''), N('さんは', '', '', [N('さん', '', ''), N('は', '', '')])])]),N('日記を捨てるような', '', '', [N('日記を', '', '', [N('日記', '', ''), N('を', '', '')]), N('捨てるような', '', '', [N('捨てる', '', ''), N('よう', '様', ''), N('な', '', '')])]),N('人じゃない', '', '', [N('人', '', ''), N('じゃ', 'だ', ''), N('ない', '無い', '')]))),
    ("としたら", ud_parsers.gendai, R(N('としたら', '', '', [N('と', '', ''), N('したら', '', '', [N('し', '為る', ''), N('たら', '', '')])]))),
    ("あいつが話の中に出てくるのが", ud_parsers.gendai, R(N('あいつが', '', '', [N('あいつ', '彼奴', ''), N('が', '', '')]), N('話の中に', '', '', [N('話の', '', '', [N('話', '', ''), N('の', '', '')]), N('中に', '', '', [N('中', '', ''), N('に', '', '')])]), N('出てくるのが', '', '', [N('出', '出る', ''), N('て', '', ''), N('くる', '来る', ''), N('の', '', ''), N('が', '', '')]))),

], ids=only_string_params)
def test_sentences_done_better_by_alternative_parser(sentence: str, parser: UDTokenizer, expected: R) -> None: run_tests(expected, parser, sentence)

# @pytest.mark.parametrize('sentence, parser, expected', [
#     ("カバンに入れっぱなしだった", ud_parsers.best, R())
# ], ids=only_string_params)
# def test_temp(sentence: str, parser: UDParser, expected: UDTextTree) -> None: run_tests(expected, parser, sentence)


def run_tests(expected:R, parser: UDTokenizer, sentence:str) -> None:
    print()
    parser = parser if parser else ud_parsers.best
    real_result = ud_tree_builder.build_tree(parser, sentence)
    spec_result = R.from_ud_tree(real_result)
    print(f"{parser.name} : {sentence}")
    print(parser.parse(sentence).to_tree())
    print()
    print("str:")
    print(str(spec_result))
    print("expected-repr:")
    print(repr(expected))
    print("repr:")
    print(repr(spec_result))
    print("repr-single-line:")
    print(repr(spec_result).replace("\n", '').replace(full_width_space, ''))

    #These seem identical. Let's find out where and how they differ by catching it here.
    assert R.from_ud_tree(ud_tree_builder.build_tree(ud_parsers.spoken, sentence)) == R.from_ud_tree(ud_tree_builder.build_tree(ud_parsers.gendai, sentence))
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
