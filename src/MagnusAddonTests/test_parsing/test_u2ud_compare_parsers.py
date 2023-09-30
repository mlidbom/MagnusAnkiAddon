import pytest
from unidic2ud import UDPipeEntry

from parsing.unidic2ud import ud2ud_parsers, ud2ud_tree_parser, ud2ud_formatter

#pytestmark = pytest.mark.skip(reason="Running exploratory code constantly is just distracting.")

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
    "ダメダメ私を助けて"
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
    # "行きたい所全部行こう",
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
    # "だったら記憶喪失の振りすることも簡単だよな"
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
