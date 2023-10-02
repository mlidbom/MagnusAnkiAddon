from typing import Any

import pytest

from parsing.universal_dependencies import ud_tree_parser, ud_parsers
from parsing.universal_dependencies.core.ud_parser import UDParser
from parsing.universal_dependencies.ud_tree_parse_result import UDTreeParseResult
from parsing.universal_dependencies.ud_tree_node import UDTreeNode

N = UDTreeNode
R = UDTreeParseResult
def only_string_params(param:Any) -> str: return param if isinstance(param, str) else ""

@pytest.mark.parametrize('sentence, expected', [
    # todo　でも, かも
    ("今じゃ町は夜でも明るいしもう会うこともないかもな",  R(N('今じゃ町は', '', [N('今じゃ', '', [N('今', ''), N('じゃ', '')]), N('町は', '', [N('町', ''), N('は', '')])]),N('夜でも明るいし', '', [N('夜でも', '', [N('夜', ''), N('で', ''), N('も', '')]), N('明るいし', '', [N('明るい', ''), N('し', '')])]),N('もう会うこと', '', [N('もう', ''), N('会うこと', '', [N('会う', ''), N('こと', '')])]),N('もないかもな', '', [N('も', ''), N('ない', '無い'), N('か', ''), N('も', ''), N('な', '')]))),
    # todo てもいい, ても
    ("食べてもいいけど", R(N('食べて', '', [N('食べ', '食べる'), N('て', '')]),N('も', ''),N('いい', '良い'),N('けど', ''))),
    # todo のに
    ("いるのにキス", R(N('いるのに', '', [N('いる', '居る'), N('の', ''), N('に', '')]), N('キス', ''))),
    # todo なかったことにして
    ("聞かなかったことにしてあげる", R(N('聞かなかったこと', '', [N('聞か', '聞く'), N('なかっ', 'ない'), N('た', ''), N('こと', '')]),N('に', ''),N('し', '為る'),N('て', ''),N('あげる', '上げる'))),

    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", R(N('ごめん自分から誘っといてちゃんと調べて', '', [N('ごめん', '御免'), N('自分から誘っといて', '', [N('自分から', '', [N('自分', ''), N('から', '')]), N('誘っといて', '', [N('誘っ', '誘う'), N('とい', 'とく'), N('て', '')])]), N('ちゃんと調べて', '', [N('ちゃんと', ''), N('調べて', '', [N('調べ', '調べる'), N('て', '')])])]), N('おけばよかった', '', [N('おけ', 'おく'), N('ば', ''), N('よかった', '', [N('よかっ', '良い'), N('た', '')])]))),
    ("探しているんですか", R(N('探して', '', [N('探し', '探す'), N('て', '')]), N('いる', '居る'), N('んです', '', [N('ん', ''), N('です', '')]), N('か', ''))),
    ("ダメダメ私を助けて", R(N('ダメダメ', ''),N('私を助けて', '', [N('私を', '', [N('私', ''), N('を', '')]), N('助けて', '', [N('助け', '助ける'), N('て', '')])]))),
    ("知らない", R(N('知らない', '',[N('知ら', '知る'), N('ない', '')]))),
    ("いつまでも来ないと知らないからね", R(N('いつまでも来ないと', '', [N('いつまでも', '', [N('いつ', ''), N('まで', ''), N('も', '')]), N('来ないと', '', [N('来', '来る'), N('ない', ''), N('と', '')])]),N('知らないからね', '', [N('知ら', '知る'), N('ない', ''), N('から', ''), N('ね', '')]))),
    ("ついに素晴らしい女性に逢えた。", R(N('ついに', '遂に'),N('素晴らしい女性に', '', [N('素晴らしい', ''), N('女性に', '', [N('女性', ''), N('に', '')])]),N('逢えた。', '', [N('逢え', '会う'), N('た', ''), N('。', '')]))),
    ("なかったかな", R(N('なかったかな', '', [N('なかっ', '無い'), N('た', ''), N('か', ''), N('な', '')]))),
    ("離れていくよ", R(N('離れて', '', [N('離れ', '離れる'), N('て', '')]),N('いく', '行く'),N('よ', ''))),
    ("夢を見た", R(N('夢を', '', [N('夢', ''), N('を', '')]),N('見た', '', [N('見', '見る'), N('た', '')]))),
    ("言われるまで気づかなかった", R(N('言われるまで', '', [N('言わ', '言う'), N('れる', ''), N('まで', '')]),N('気づかなかった', '', [N('気づか', '気付く'), N('なかっ', 'ない'), N('た', '')]))),
    ("行きたい所全部行こう", R(N('行きたい所', '', [N('行きたい', '', [N('行き', '行く'), N('たい', '')]), N('所', '')]),N('全部行こう', '全部行く', [N('全部', ''), N('行こう', '行く')]))),
    ("当てられても", R(N('当てられても', '', [N('当て', '当てる'), N('られ', 'られる'), N('て', ''), N('も', '')]))),
    ("逃げたり", R(N('逃げたり', '',[N('逃げ', '逃げる'), N('たり', '')]))),
    ("するためでした", R(N('するためでした', '', [N('する', '為る'), N('ためでした', '', [N('ため', '為'), N('でし', 'です'), N('た', '')])]))),
    ("ように言ったのも", R(N('ように', 'ようだ', [N('よう', ''), N('に', 'だ')]),N('言ったのも', '', [N('言っ', '言う'), N('た', ''), N('の', ''), N('も', '')]))),
    ("一度聞いたことがある", R(N('一度聞いたこと', '', [N('一度', ''), N('聞いたこと', '', [N('聞い', '聞く'), N('た', ''), N('こと', '')])]),N('がある', 'が有る', [N('が', ''), N('ある', '有る')]))),
    ("よかった", R(N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
    ("友達だから余計に気になっちゃうんだよ", R(N('友達だから余計に気になっちゃうん', '', [N('友達だから', '', [N('友達', ''), N('だ', ''), N('から', '')]), N('余計に', '余計だ', [N('余計', ''), N('に', 'だ')]), N('気になっちゃうん', '', [N('気に', '', [N('気', ''), N('に', '')]), N('なっちゃうん', '', [N('なっ', '成る'), N('ちゃう', ''), N('ん', '')])])]),N('だよ', '', [N('だ', ''), N('よ', '')]))),
    ("自分のことを知ってもらえてない人に", R(N('自分のことを', '', [N('自分の', '', [N('自分', ''), N('の', '')]), N('ことを', '', [N('こと', ''), N('を', '')])]),N('知ってもらえてない人に', '', [N('知って', '', [N('知っ', '知る'), N('て', '')]), N('もらえ', '貰う'), N('て', 'てる'), N('ない', ''), N('人に', '', [N('人', ''), N('に', '')])]))),
    ("よかった", R(N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
    ("良かった", R(N('良かった', '', [N('良かっ', '良い'), N('た', '')]))),
    ("良くない", R(N('良くない', '良く無い', [N('良く', '良い'), N('ない', '無い')]))),
    ("良ければ", R(N('良ければ', '', [N('良けれ', '良い'), N('ば', '')]))),
    ("良かったら", R(N('良かったら', '良かった', [N('良かっ', '良い'), N('たら', 'た')]))),
    ("よかったじゃん", R(N('よかったじゃん', '', [N('よかっ', '良い'), N('た', ''), N('じゃん', '')]))),
    ("言えばよかった", R(N('言えば', '', [N('言え', '言う'), N('ば', '')]), N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
   ], ids=only_string_params)
def test_sentences_the_best_parser_does_well(sentence: str, expected: UDTreeParseResult) -> None: run_tests(expected, ud_parsers.best, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    ("ううん藤宮さんは日記を捨てるような人じゃない", ud_parsers.gendai, R(N('ううん藤宮さんは', '', [N('ううん', ''), N('藤宮さんは', '', [N('藤宮', 'フジミヤ'), N('さんは', '', [N('さん', ''), N('は', '')])])]),N('日記を捨てるような', '日記を捨てるようだ', [N('日記を', '', [N('日記', ''), N('を', '')]), N('捨てるような', '捨てるようだ', [N('捨てる', ''), N('よう', '様'), N('な', 'だ')])]),N('人じゃない', '人じゃ無い', [N('人', ''), N('じゃ', 'だ'), N('ない', '無い')]))),
    ("としたら", ud_parsers.gendai,  R(N('としたら', 'とした', [N('と', ''), N('したら', 'した', [N('し', '為る'), N('たら', 'た')])]))),
    ("あいつが話の中に出てくるのが", ud_parsers.gendai, R(N('あいつが', '', [N('あいつ', '彼奴'), N('が', '')]), N('話の中に', '', [N('話の', '', [N('話', ''), N('の', '')]), N('中に', '', [N('中', ''), N('に', '')])]), N('出てくるのが', '', [N('出', '出る'), N('て', ''), N('くる', '来る'), N('の', ''), N('が', '')]))),

], ids=only_string_params)
def test_sentences_done_better_by_alternative_parser(sentence: str, parser: UDParser, expected: UDTreeParseResult) -> None: run_tests(expected, parser, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
], ids=only_string_params)
def test_temp(sentence: str, parser: UDParser, expected: UDTreeParseResult) -> None: run_tests(expected, parser, sentence)


def run_tests(expected:UDTreeParseResult, parser: UDParser, sentence:str) -> None:
    print()
    parser = parser if parser else ud_parsers.best
    result = ud_tree_parser.parse(parser, sentence)
    print(f"{parser.name} : {sentence}")
    print(parser.parse(sentence).to_tree())
    print()
    print("str:")
    print(str(result))
    print("expected-repr:")
    print(repr(expected))
    print("repr:")
    print(repr(result))
    print("repr-single-line:")
    print(repr(result).replace("\n", "").replace("　", ""))

    #These are neck and neck. Let's find out where and how they differ by catching it here.
    assert ud_tree_parser.parse(ud_parsers.spoken, sentence) == ud_tree_parser.parse(ud_parsers.gendai, sentence)
    assert result == expected






@pytest.mark.parametrize("sentence", [
    # "朝、近所をぶらぶらした。",
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
    #"食べてもいいけど"
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
        print(ud_tree_parser.parse(parser, sentence))
        print()
