import pytest

from parsing.universal_dependencies import ud2ud_tree_parser, ud2ud_parsers
from parsing.universal_dependencies.ud2ud_parsers import UDParser
from parsing.universal_dependencies.ud2ud_tree_parser_result import UD2UDParseResult
from parsing.universal_dependencies.ud2ud_tree_node import UD2UDTreeNode

N = UD2UDTreeNode
R = UD2UDParseResult
def only_string_params(param) -> str: return param if isinstance(param, str) else ""

@pytest.mark.parametrize('sentence, parser, expected', [
    # todo　でも, かも
    ("今じゃ町は夜でも明るいしもう会うこともないかもな", None, R(N('今じゃ町は夜でも明るいし', '', [N('今じゃ', '今で', [N('今', ''), N('じゃ', 'で')]), N('町は', '', [N('町', ''), N('は', '')]), N('夜でも明るいし', '', [N('夜でも', '', [N('夜', ''), N('で', ''), N('も', '')]), N('明るいし', '', [N('明るい', ''), N('し', '')])])]), N('もう会う', '', [N('もう', ''), N('会う', '')]), N('こともないかもな', '', [N('ことも', '', [N('こと', '事'), N('も', '')]), N('ないかもな', '', [N('ない', '無い'), N('か', ''), N('も', ''), N('な', '')])]))),
    # todo てもいい, ても
    ("食べてもいいけど", None, R(N('食べても', '', [N('食べ', '食べる'), N('て', ''), N('も', '')]), N('いいけど', 'いいけれど', [N('いい', '良い'), N('けど', 'けれど')]))),
    # todo のに
    ("いるのにキス", None, R(N('いるのに', '', [N('いる', '居る'), N('の', ''), N('に', '')]), N('キス', ''))),
    # todo: んです
    ("探しているんですか", None, R(N('探しているんですか', '', [N('探し', '探す'), N('て', ''), N('いる', '居る'), N('ん', 'の'), N('です', ''), N('か', '')]))),
    # todo おけばよかった
    ("ごめん　自分から誘っといて ちゃんと調べておけばよかった", None, R(N('ごめん自分から', '', [N('ごめん', '御免'), N('自分から', '', [N('自分', ''), N('から', '')])]), N('誘っといてちゃんと調べておけば', '', [N('誘っといて', '', [N('誘っ', '誘う'), N('とい', 'とく'), N('て', '')]), N('ちゃんと調べておけば', '', [N('ちゃんと', ''), N('調べておけば', '', [N('調べ', '調べる'), N('て', ''), N('おけ', '置く'), N('ば', '')])])]), N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
    # todo なかったことにして
    ("聞かなかったことにしてあげる", None, R(N('聞かなかった', '', [N('聞か', '聞く'), N('なかっ', 'ない'), N('た', '')]), N('ことにしてあげる', 'ことにして上げる', [N('こと', '事'), N('に', ''), N('し', '為る'), N('て', ''), N('あげる', '上げる')]))),

    # todo: ダメダメ
    ("ダメダメ私を助けて", None, R(N('ダメ', '駄目'), N('ダメ', '駄目'), N('私を助けて', '', [N('私を', '', [N('私', ''), N('を', '')]), N('助けて', '', [N('助け', '助ける'), N('て', '')])]))),
    ("ダメダメ私を助けて", ud2ud_parsers.default, R(N('ダメダメ私を', '', [N('ダメダメ', 'ダメ駄目'), N('私を', '', [N('私', ''), N('を', '')])]), N('助けて', '', [N('助け', '助ける'), N('て', '')]))),
    ("ダメダメ私を助けて", ud2ud_parsers.qkana, R(N('ダメダメ私を', '', [N('ダメダメ', ''), N('私を', '', [N('私', ''), N('を', '')])]), N('助けて', '', [N('助け', '助ける'), N('て', '')]))),
    ("ダメダメ私を助けて", ud2ud_parsers.kindai, R(N('ダメダメ', ''), N('私を助けて', '', [N('私を', '', [N('私', ''), N('を', '')]), N('助けて', '', [N('助け', '助ける'), N('て', '')])]))),
    ("ダメダメ私を助けて", ud2ud_parsers.kinsei, R(N('ダメダメ', ''), N('私を助けて', '', [N('私を', '', [N('私', ''), N('を', '')]), N('助けて', '', [N('助け', '助ける'), N('て', '')])]))),


    ("知らない", None, R(N('知らない', '',[N('知ら', '知る'), N('ない', '')]))),
    ("いつまでも来ないと知らないからね", None, R(N('いつまでも来ないと', '', [N('いつまでも', '', [N('いつ', '何時'), N('まで', ''), N('も', '')]), N('来ないと', '', [N('来', '来る'), N('ない', ''), N('と', '')])]),N('知らないからね', '', [N('知ら', '知る'), N('ない', ''), N('から', ''), N('ね', '')]))),
    ("ついに素晴らしい女性に逢えた。", None, R(N('ついに', '遂に'),N('素晴らしい女性に', '', [N('素晴らしい', ''), N('女性に', '', [N('女性', ''), N('に', '')])]),N('逢えた。', '', [N('逢え', '会う'), N('た', ''), N('。', '')]))),
    ("ううん藤宮さんは日記を捨てるような人じゃない", None, R(N('ううん藤宮さんは', '', [N('ううん', ''), N('藤宮さんは', '', [N('藤宮', 'フジミヤ'), N('さんは', '', [N('さん', ''), N('は', '')])])]),N('日記を捨てるような', '日記を捨てるようだ', [N('日記を', '', [N('日記', ''), N('を', '')]), N('捨てるような', '捨てるようだ', [N('捨てる', ''), N('よう', '様'), N('な', 'だ')])]),N('人じゃない', '人じゃ無い', [N('人', ''), N('じゃ', 'だ'), N('ない', '無い')]))),
    ("なかったかな", None, R(N('なかったかな', '', [N('なかっ', '無い'), N('た', ''), N('か', ''), N('な', '')]))),
    ("としたら", None,  R(N('としたら', 'とした', [N('と', ''), N('したら', 'した', [N('し', '為る'), N('たら', 'た')])]))),
    ("離れていくよ", None,  R(N('離れていくよ', '', [N('離れ', '離れる'), N('て', ''), N('いく', '行く'), N('よ', '')]))),
    ("夢を見た", None, R(N('夢を', '', [N('夢', ''), N('を', '')]),N('見た', '', [N('見', '見る'), N('た', '')]))),
    ("言われるまで気づかなかった", None, R(N('言われるまで', '', [N('言わ', '言う'), N('れる', ''), N('まで', '')]),N('気づかなかった', '', [N('気づか', '気付く'), N('なかっ', 'ない'), N('た', '')]))),
    ("行きたい所全部行こう", None, R(N('行きたい所', '', [N('行きたい', '', [N('行き', '行く'), N('たい', '')]), N('所', '')]),N('全部行こう', '全部行く', [N('全部', ''), N('行こう', '行く')]))),
    ("当てられても", None, R(N('当てられても', '', [N('当て', '当てる'), N('られ', 'られる'), N('て', ''), N('も', '')]))),
    ("逃げたり", None, R(N('逃げたり', '',[N('逃げ', '逃げる'), N('たり', '')]))),
    ("するためでした", None, R(N('するためでした', '', [N('する', '為る'), N('ためでした', '', [N('ため', '為'), N('でし', 'です'), N('た', '')])]))),
    ("ように言ったのも", None, R(N('ように', 'ようだ', [N('よう', '様'), N('に', 'だ')]),N('言ったのも', '', [N('言っ', '言う'), N('た', ''), N('の', ''), N('も', '')]))),
    ("一度聞いたことがある", None, R(N('一度', '', [N('一', ''), N('度', '')]),N('聞いたことが', '', [N('聞いた', '', [N('聞い', '聞く'), N('た', '')]), N('ことが', '', [N('こと', '事'), N('が', '')])]),N('ある', '有る'))),
    ("よかった", None, R(N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
    ("友達だから余計に気になっちゃうんだよ", None, R(N('友達だから余計に', '友達だから余計だ', [N('友達だから', '', [N('友達', ''), N('だ', ''), N('から', '')]), N('余計に', '余計だ', [N('余計', ''), N('に', 'だ')])]),N('気になっちゃうんだよ', '', [N('気に', '', [N('気', ''), N('に', '')]), N('なっちゃうんだよ', '', [N('なっ', '成る'), N('ちゃう', ''), N('ん', 'の'), N('だ', ''), N('よ', '')])]))),
   ], ids=only_string_params)
def test_various_stuff(sentence: str, parser: UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    # various conjugations
    ("よかった", None, R(N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
    ("良かった", None, R(N('良かった', '',[N('良かっ', '良い'), N('た', '')]))),
    ("良くない", None, R(N('良くない', '良く無い', [N('良く', '良い'), N('ない', '無い')]))),
    ("良ければ", None, R(N('良ければ', '',[N('良けれ', '良い'), N('ば', '')]))),
    ("良かったら", None, R(N('良かったら', '良かった',[N('良かっ', '良い'), N('たら', 'た')]))),
    ("よかったじゃん", None, R(N('よかったじゃん', '', [N('よかっ', '良い'), N('た', ''), N('じゃん', '')]))),

    # adjective within verb compound
    ("言えばよかった", None, R(N('言えば', '', [N('言え', '言う'), N('ば', '')]),N('よかった', '', [N('よかっ', '良い'), N('た', '')]))),
], ids=only_string_params)
def test_adjective_compounds(sentence: str, parser: UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)


@pytest.mark.parametrize('sentence, parser, expected', [
    ("あいつが話の中に出てくるのが", None, R(N('あいつが', '', [N('あいつ', '彼奴'), N('が', '')]),N('話の中に', '', [N('話の', '', [N('話', ''), N('の', '')]), N('中に', '', [N('中', ''), N('に', '')])]),N('出てくるのが', '', [N('出', '出る'), N('て', ''), N('くる', '来る'), N('の', ''), N('が', '')]))),
    ("自分のことを知ってもらえてない人に", None, R(N('自分のことを', '', [N('自分の', '', [N('自分', ''), N('の', '')]), N('ことを', '', [N('こと', '事'), N('を', '')])]),N('知ってもらえてない人に', '', [N('知ってもらえてない', '', [N('知っ', '知る'), N('て', ''), N('もらえ', '貰う'), N('て', 'てる'), N('ない', '')]), N('人に', '', [N('人', ''), N('に', '')])]))),
], ids=only_string_params)
def test_noun_compounds(sentence: str, parser: UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
], ids=only_string_params)
def test_temp(sentence: str, parser: UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)


def run_tests(expected:UD2UDParseResult, parser: UDParser, sentence:str) -> None:
    print()
    parser = parser if parser else ud2ud_parsers.best
    result = ud2ud_tree_parser.parse(parser, sentence)
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
    assert ud2ud_tree_parser.parse(ud2ud_parsers.spoken, sentence) == ud2ud_tree_parser.parse(ud2ud_parsers.gendai, sentence)
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
    for parser in ud2ud_parsers.all_parsers:
        print(f"{parser.name} : {sentence}")
        print(parser.parse(sentence).to_tree())
        print()

    for parser in ud2ud_parsers.all_parsers:
        print(f"{parser.name} : {sentence}")
        print(ud2ud_tree_parser.parse(parser, sentence))
        print()
