import pytest
from unidic2ud import UDPipeEntry

import unidic2ud_formatter
from src.ExploratoryTests.unidic2ud import u2udtreeparser, ud2ud_parsers

#pytestmark = pytest.mark.skip(reason="Running exploratory code constantly is just distracting.")

_parsers = [ud2ud_parsers.gendai,  # The leader so far
            ud2ud_parsers.kindai,  # seems slightly less accurate than gendai.
            ud2ud_parsers.default,  # As alternative? When differing from kindai, usually seems worse but significantly different. Polarity negative feature. Good for something?
            # ("spoken", (unidic2ud.load("spoken"))), # todo Recheck
            # ("kinsei_edo", (unidic2ud.load("kinsei\\50c_kinsei-edo"))), # todo Recheck
            # ("kinsei_kindai_bungo", (unidic2ud.load("kinsei\\60a_kindai-bungo"))), # todo Recheck
            # ("novel", (unidic2ud.load("novel"))), # todo Recheck
            # ("qkana", (unidic2ud.load("qkana"))), # todo Recheck
            # ("kyogen", (unidic2ud.load("kyogen"))), # todo Recheck
            # ("wakan", (unidic2ud.load("wakan"))), #No. wakan gives wack results
            # ("wabun", (unidic2ud.load("wabun"))), #No. oddness abounds
            # ("manyo", (unidic2ud.load("manyo"))) #No. seems to usually give some truly strange results
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
        print(parser.name)
        print(parser.parse(common_sentence).to_tree())
        print(u2udtreeparser.parse(parser, common_sentence))
        print()


    # for parser_name, result in results:
    #     print(parser_name)
    #     print(unidic2ud_formatter.format_output(result))

    # for parser_name, result_tokens in result_list_tokens:
    #     print(f"{parser_name} : {common_sentence}")
    #     print(u2udtreeparser.parse(result_tokens))
    #     print()
    #
    # name, parser = _parsers[2]
    # step1 = parser(common_sentence)
    # parsed = u2udtreeparser.parse(step1)
    # print()
    # print(step1.to_tree())
    # print(parsed)

def test_build_tree(common_sentence: str) -> None:
    results = [(parser.name, parser.parse(common_sentence)) for parser in _parsers]

    result_list_tokens: list[tuple[str, list[UDPipeEntry]]] = [(name, [tok for tok in result]) for name, result in results]

    print()
    print(common_sentence)
    for parser_name, result in results:
        print(parser_name)
        print(result.to_tree())

    for depth in [3, 2, 1, 0]:
        for parser_name, result_tokens in result_list_tokens:
            print_tree(f"depth: {depth} {parser_name}", tree_parse_algorithm_1(result_tokens, depth))



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



def _consume_children_of(entry:UDPipeEntry, tokens:list[UDPipeEntry]) -> int:
    index = 0
    for current_token in tokens:
        if _head(current_token).id != entry.id:
            break
        index += 1
    return index

def _consume_until(entry:UDPipeEntry, tokens:list[UDPipeEntry]) -> int:
    index = 0
    for current_token in tokens:
        if current_token.id == entry.id:
            break
        index += 1
    return index

def tree_parse_algorithm_1(result_tokens:list[UDPipeEntry], depth:int) -> list[UDPipeEntry]:
    compounds: list[UDPipeEntry] = []

    remaining_tokens = result_tokens[1:]  # The first is some empty thingy we don't want.
    while remaining_tokens:
        compound_start = remaining_tokens[0]
        compound_head: UDPipeEntry = _head(compound_start)
        token_index = 1

        token_index += _consume_children_of(compound_start, remaining_tokens[token_index:])

        if depth >= 3:
            token_index += _consume_until(compound_head, remaining_tokens[token_index:])

        if len(remaining_tokens) > token_index:
            if (depth >= 3
                    or depth >= 2
                    or depth >= 1 and compound_head.id == compound_start.id + 1):
                current_token = remaining_tokens[token_index]
                if current_token.id == compound_head.id:
                    token_index += 1
                    token_index += _consume_children_of(compound_head, remaining_tokens[token_index:])

        consumed_tokens = remaining_tokens[:token_index]
        remaining_tokens = remaining_tokens[token_index:]
        compounds.append(consumed_tokens)
    return compounds

def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa


