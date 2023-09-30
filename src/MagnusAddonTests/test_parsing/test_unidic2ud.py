import pytest
from unidic2ud import UDPipeEntry

from parsing.unidic2ud import u2udtreeparser, ud2ud_parsers
from test_parsing import unidic2ud_formatter

#pytestmark = pytest.mark.skip(reason="Running exploratory code constantly is just distracting.")

_parsers = [ud2ud_parsers.gendai,  # The leader so far
            ud2ud_parsers.kindai,  # seems slightly less accurate than gendai.
            ud2ud_parsers.default,  # As alternative? When differing from kindai, usually seems worse but significantly different. Polarity negative feature. Good for something?
            #ud2ud_parsers.spoken, # todo Recheck
            #ud2ud_parsers.kinsei, # todo Recheck
            #ud2ud_parsers.novel, # todo Recheck
            #ud2ud_parsers.qkana, # todo Recheck
            #ud2ud_parsers.kyogen, # todo Recheck
            #ud2ud_parsers.wakan, #No. wakan gives wack results
            #ud2ud_parsers.wabun, #No. oddness abounds
            #ud2ud_parsers.manyo #No. seems to usually give some truly strange results
            ]


@pytest.fixture(params=[
    "朝、近所をぶらぶらした。",
    "そんなに気になるなら あの時俺も友達だって言えばよかったじゃん",
    "普段どうやって日記読んでたんだ",
    "何か意味があるんだと思う",
    "いつまでも来ないと知らないからね",
    "離れていくよ",
    "ああだからあの時忘れんなって言ったのに",
    "ダメダメ私を助けて",
    "ついに素晴らしい女性に逢えた。",
    "ううん藤宮さんは日記を捨てるような人じゃない",
    "探しているんですか",
    "行きたい所全部行こう",
    "一度聞いたことがある",
    "よかったじゃん",
    "言えばよかった",
    "言われるまで気づかなかった",
    "夢を見た",
    "知らない",
    "何よあの態度偉そうに",
    "これから本題に入るんだけど",
    "食べられるもの",
    "俺以外に友達がいなくてよかったとか　絶対思っちゃダメなのに",
    "日代さんが 先生に知らせてくれたらしい",
    "やっぱりあの噂ホントだったんだ",
    "だったら記憶喪失の振りすることも簡単だよな",
    "だったら記憶喪失の振りすることも簡単だよな"
])
def common_sentence(request) -> str: return request.param


def test_just_display_various_sentences(common_sentence: str) -> None:
    run_tests(common_sentence)

def test_tree_parser(common_sentence: str) -> None:
    results = [(parser.name, parser.parse(common_sentence)) for parser in _parsers]

    print()
    print(common_sentence)
    for parser in _parsers:
        print(f"{parser.name} : {common_sentence}")
        print(parser.parse(common_sentence).to_tree())
        print()

    for parser in _parsers:
        print(f"{parser.name} : {common_sentence}")
        print(u2udtreeparser.parse(parser, common_sentence))
        print()

def print_tree(name:str, tree:list[UDPipeEntry]) -> None:
    print(name)
    for compound in tree:
        consumed_forms = [f.form for f in compound]
        print("".join(consumed_forms))
    print()


def run_tests(sentence) -> None:
    results = [(parser.name, parser.parse(sentence)) for parser in _parsers]

    for name, result in results:
        if hasattr(result, "to_tree") and callable(result.to_tree):
            print()
            print(f"{name}: {sentence}")
            print(result.to_tree())
        else:
            print()
            print(f"""{name} has no to_tree() method""")

    for name, result in results:
        print()
        print(f"{name}: {sentence}")
        print(unidic2ud_formatter.format_output(result))

    reference_name, reference_result = results[0]
    current_name, current_result = results[1]

    assert unidic2ud_formatter.format_output_for_comparing_ignore_space_after_and_features(current_result) == unidic2ud_formatter.format_output_for_comparing_ignore_space_after_and_features(reference_result)


