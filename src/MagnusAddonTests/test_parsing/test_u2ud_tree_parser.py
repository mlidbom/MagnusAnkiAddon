import pytest

from parsing.unidic2ud import ud2ud_tree_parser, ud2ud_parsers
from parsing.unidic2ud.ud2ud_parsers import UD2UDParser
from parsing.unidic2ud.ud2ud_tree_parser_result import UD2UDParseResult
from parsing.unidic2ud.ud2ud_tree_node import UD2UDTreeNode

N = UD2UDTreeNode
R = UD2UDParseResult
def only_string_params(param) -> str: return param if isinstance(param, str) else ""

@pytest.mark.parametrize('sentence, parser, expected', [
    ("知らない", None, R(N('知らない', '',[N('知ら', '知る'), N('ない', '')]))),
    ("いつまでも来ないと知らないからね", None, R(N('いつまでも来ないと', '', [N('いつまでも', '', [N('いつ', '何時'), N('まで', ''), N('も', '')]), N('来ないと', '', [N('来', '来る'), N('ない', ''), N('と', '')])]),N('知らないからね', '', [N('知ら', '知る'), N('ない', ''), N('から', ''), N('ね', '')]))),
    ("ついに素晴らしい女性に逢えた。", None, R(N('ついに', '遂に'),N('素晴らしい女性に', '', [N('素晴らしい', ''), N('女性に', '', [N('女性', ''), N('に', '')])]),N('逢えた。', '', [N('逢え', '会う'), N('た', ''), N('。', '')]))),
    ("ううん藤宮さんは日記を捨てるような人じゃない", None, R(N('ううん藤宮さんは', '', [N('ううん', ''), N('藤宮さんは', '', [N('藤宮', 'フジミヤ'), N('さんは', '', [N('さん', ''), N('は', '')])])]),N('日記を捨てるような', '日記を捨てるようだ', [N('日記を', '', [N('日記', ''), N('を', '')]), N('捨てるような', '捨てるようだ', [N('捨てる', ''), N('よう', '様'), N('な', 'だ')])]),N('人じゃない', '人じゃ無い', [N('人', ''), N('じゃ', 'だ'), N('ない', '無い')]))),
    ("なかったかな", ud2ud_parsers.kindai, R(N('なかったかな', 'なかった哉', [N('なかっ', '無い'), N('た', ''), N('かな', '哉')]))),
    ("探しているんですか", None, R(N('探しているんですか', '', [N('探し', '探す'), N('て', ''), N('いる', '居る'), N('ん', 'の'), N('です', ''), N('か', '')]))),
    ("としたら", None,  R(N('としたら', 'とした', [N('と', ''), N('し', '為る'), N('たら', 'た')]))),
    ("離れていくよ", None,  R(N('離れていくよ', '', [N('離れ', '離れる'), N('て', ''), N('いく', '行く'), N('よ', '')]))),
    ("いつまでも来ないと知らないからね", None,  R(N('いつまでも来ないと', '', [N('いつまでも', '', [N('いつ', '何時'), N('まで', ''), N('も', '')]), N('来ないと', '', [N('来', '来る'), N('ない', ''), N('と', '')])]),N('知らないからね', '', [N('知ら', '知る'), N('ない', ''), N('から', ''), N('ね', '')]))),
    ("ダメダメ私を助けて", ud2ud_parsers.kindai,  R(N('ダメダメ', ''),N('私を助けて', '', [N('私を', '', [N('私', ''), N('を', '')]), N('助けて', '', [N('助け', '助ける'), N('て', '')])]))),
    ("夢を見た", None, R(N('夢を', '', [N('夢', ''), N('を', '')]),N('見た', '', [N('見', '見る'), N('た', '')]))),
    ("言われるまで気づかなかった", None, R(N('言われるまで', '', [N('言わ', '言う'), N('れる', ''), N('まで', '')]),N('気づかなかった', '', [N('気づか', '気付く'), N('なかっ', 'ない'), N('た', '')]))),
    ("行きたい所全部行こう", None, R(N('行きたい所', '', [N('行きたい', '', [N('行き', '行く'), N('たい', '')]), N('所', '')]),N('全部行こう', '全部行く', [N('全部', ''), N('行こう', '行く')]))),
    ("当てられても", None, R(N('当てられても', '', [N('当て', '当てる'), N('られ', 'られる'), N('て', ''), N('も', '')]))),
    # todo Could we get the ても merged?
    ("食べてもいいけど", None, R(N('食べても', '', [N('食べ', '食べる'), N('て', ''), N('も', '')]),N('いいけど', 'いいけれど', [N('いい', '良い'), N('けど', 'けれど')]))),
    ("逃げたり", None, R(N('逃げたり', '',[N('逃げ', '逃げる'), N('たり', '')]))),
    # todo could we get the のに merged?
    ("いるのにキス", None, R(N('いるのに', '', [N('いる', '居る'), N('の', ''), N('に', '')]),N('キス', ''))),
    ("するためでした", None, R(N('する', ''), N('ため', ''), N('でし', 'です'), N('た', ''))),
    #("ように言ったのも", None, R(N('ように言った', '',[N('ように言っ', 'ように言う',[N('ように', '',[N('よう', ''), N('に', '')]), N('言っ', '言う')]), N('た', '')]), N('の', ''), N('も', ''))),
    #("探しているんですか", None, R(N('探している', '',[N('探し', '探す'), N('て', ''), N('いる', '')]), N('んです', '',[N('ん', ''), N('です', '')]), N('か', ''))),
    #("一度聞いたことがある", None, R(N('一度', ''), N('聞いたことがある', '',[N('聞い', '聞く'), N('た', ''), N('ことがある', '',[N('こと', ''), N('が', ''), N('ある', '')])]))),
    #("よかった", None, R(N('よかった', '',[N('よかっ', 'よい'), N('た', '')]))),
    #("聞かなかったことにしてあげる", None, R(N('聞かなかったことにしてあげる', '',[N('聞か', '聞く'), N('なかったことにし', 'なかったことにする',[N('なかっ', 'ない'), N('た', ''), N('ことにし', 'ことにする',[N('こと', ''), N('にし', 'にする',[N('に', ''), N('し', 'する')])])]), N('て', ''), N('あげる', '')]))),
    #("明るいしもう", None, R(N('明るいし', '明るいする',[N('明るい', ''), N('し', 'する')]), N('もう', '',[N('も', ''), N('う', '')]))),
    #("今じゃ町は夜でも明るいしもう会うこともないかもな", None, R(N('今じゃ', '',[N('今', ''), N('じゃ', '')]), N('町は', '',[N('町', ''), N('は', '')]), N('夜でも', '',[N('夜', ''), N('でも', '')]), N('明るいし', '',[N('明るい', ''), N('し', '')]), N('もう', ''), N('会うこともないかも', '',[N('会う', ''), N('こと', ''), N('も', ''), N('ない', ''), N('かも', '')]), N('な', ''))),
    #("友達だから余計に気になっちゃうんだよ", None, R(N('友達だから', '',[N('友達', ''), N('だから', '',[N('だ', ''), N('から', '')])]), N('余計に', '',[N('余計', ''), N('に', '')]), N('気になっちゃうんだよ', '',[N('気になっ', '気になる',[N('気', ''), N('に', ''), N('なっ', 'なる')]), N('ちゃう', ''), N('んだ', '',[N('ん', ''), N('だ', '')]), N('よ', '')]))),
], ids=only_string_params)
def test_various_stuff(sentence: str, parser: UD2UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    # various conjugations
    #("よかった", None, R(N('よかった', '',[N('よかっ', 'よい'), N('た', '')]))),
    #("良かった", None, R(N('良かった', '',[N('良かっ', '良い'), N('た', '')]))),
    #("良くない", None, R(N('良くない', '',[N('良く', '良い'), N('ない', '')]))),
    #("良ければ", None, R(N('良ければ', '',[N('良けれ', '良い'), N('ば', '')]))),
    #("良かったら", None, R(N('良かったら', '良かった',[N('良かっ', '良い'), N('たら', 'た')]))),
    #("よかったじゃん", None, R(N('よかった', '',[N('よかっ', 'よい'), N('た', '')]), N('じゃん', ''))),

    # adjective within verb compound
    #("言えばよかった", None, R(N('言えば', '',[N('言え', '言う'), N('ば', '')]), N('よかった', '',[N('よかっ', 'よい'), N('た', '')]))),
], ids=only_string_params)
def test_adjective_compounds(sentence: str, parser: UD2UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)


@pytest.mark.parametrize('sentence, parser, expected', [
    #("あいつが話の中に出てくるのが", None, R(N('あいつが', '',[N('あいつ', ''), N('が', '')]), N('話の中に', '',[N('話', ''), N('の', ''), N('中', ''), N('に', '')]), N('出てくるのが', '',[N('出てくるの', '',[N('出てくる', '',[N('出', '出る'), N('て', ''), N('くる', '')]), N('の', '')]), N('が', '')]))),
    #("自分のことを知ってもらえてない人に", None, R(N('自分のことを', '',[N('自分', ''), N('の', ''), N('こと', ''), N('を', '')]), N('知ってもらえてない人に', '',[N('知ってもらえてない人', '',[N('知っ', '知る'), N('て', ''), N('もらえ', 'もらう'), N('て', 'てる'), N('ない', ''), N('人', '')]), N('に', '')]))),
], ids=only_string_params)
def test_noun_compounds(sentence: str, parser: UD2UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)

@pytest.mark.parametrize('sentence, parser, expected', [
    #("今じゃ町は夜でも明るいしもう会うこともないかもな", None, R(N('今じゃ', '',[N('今', ''), N('じゃ', '')]), N('町は', '',[N('町', ''), N('は', '')]), N('夜でも', '',[N('夜', ''), N('でも', '')]), N('明るいし', '',[N('明るい', ''), N('し', '')]), N('もう', ''), N('会うこともないかも', '',[N('会う', ''), N('こと', ''), N('も', ''), N('ない', ''), N('かも', '')]), N('な', '')))
], ids=only_string_params)
def test_temp(sentence: str, parser: UD2UDParser, expected: UD2UDParseResult) -> None: run_tests(expected, parser, sentence)


def run_tests(expected:UD2UDParseResult, parser: UD2UDParser, sentence:str) -> None:
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
    assert result == expected



_parsers = [ud2ud_parsers.gendai,  # The leader so far
            ud2ud_parsers.kindai,  # seems slightly less accurate than gendai.
            ud2ud_parsers.default,  # As alternative? When differing from kindai, usually seems worse but significantly different. Polarity negative feature. Good for something?
            ud2ud_parsers.spoken, # todo Recheck
            ud2ud_parsers.kinsei, # todo Recheck
            ud2ud_parsers.novel, # todo Recheck
            ud2ud_parsers.qkana, # todo Recheck
            ud2ud_parsers.kyogen, # todo Recheck
            ud2ud_parsers.wakan, #No. wakan gives wack results
            ud2ud_parsers.wabun, #No. oddness abounds
            ud2ud_parsers.manyo #No. seems to usually give some truly strange results
            ]


@pytest.mark.parametrize("sentence", [
    #"ダメダメ私を助けて"
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
    for parser in _parsers:
        print(f"{parser.name} : {sentence}")
        print(parser.parse(sentence).to_tree())
        print()

    for parser in _parsers:
        print(f"{parser.name} : {sentence}")
        print(ud2ud_tree_parser.parse(parser, sentence))
        print()
