import pytest
import unidic2ud
from _pytest.fixtures import FixtureRequest
from unidic2ud import UniDic2UDEntry, UniDic2UD, UDPipeEntry

#pytestmark = pytest.mark.skip(reason="Running exploratory code constantly is just distracting.")

_parsers:list[tuple[str, UniDic2UD]] = []

@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global _parsers
    _parsers = [("kindai", (unidic2ud.load("kindai"))),  # The leader so for
                ("gendai", (unidic2ud.load("gendai"))),  # seems neck and neck with kindai.
                ("default", (unidic2ud.load())),  # As alternative? When differing from kindai, usually seems worse but significantly different. Polarity negative feature. Good for something?
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
    "知らない"
])
def common_sentence(request) -> str: return request.param


def test_just_display_various_sentences(common_sentence: str) -> None:
    run_tests(common_sentence)

def test_build_tree(common_sentence: str) -> None:
    parser = _parsers[0][1]
    parser_name = _parsers[0][0]
    print()
    print(parser_name)

    parse_result = parser(common_sentence)
    print(parse_result.to_tree())

    result_tokens:list[UDPipeEntry] = [tok for tok in parse_result]
    print(result_tokens)

    tree:list[str] = []

    remaining_tokens = result_tokens[1:] #The first is some empty thingy we don't want.
    while remaining_tokens:
        first_remaining = remaining_tokens[0]
        target_head:UDPipeEntry = _head(first_remaining)

        token_index = 1

        for token in remaining_tokens[1:]: #consume tokens that have first_remaining as their head
            if _head(token).id != first_remaining.id:
                break

            token_index += 1

        for token in remaining_tokens[1:]: #consume tokens up until we find the target head
            token_index += 1
            if token.id == target_head.id: # we found our target head, continue only through tokens with this head
                for tail_token in remaining_tokens[token_index:]:
                    if _head(tail_token).id != target_head.id:
                        break
                    token_index += 1

                break

        consumed_tokens = remaining_tokens[:token_index]
        remaining_tokens = remaining_tokens[token_index:]
        consumed_forms = [f.form for f in consumed_tokens]
        tree.append("".join(consumed_forms))


    print("Here's the tree")
    for line in tree:
        print(line)

def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa

def run_tests(sentence) -> None:
    results = [(name, parser(sentence)) for name, parser in _parsers]

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
        print(format_output(result))

    reference_name, reference_result = results[0]
    current_name, current_result = results[1]

    assert format_output_for_comparing_ignore_space_after_and_features(current_result) == format_output_for_comparing_ignore_space_after_and_features(reference_result)



def format_output(entry: 'UniDic2UDEntry') -> str:  # Replace 'UniDic2UDEntry' with your actual type
    line_rows = get_line_rows(entry)
    return align_tab_separated_values(line_rows)

def format_output_for_comparing_ignore_space_after_and_features(entry: 'UniDic2UDEntry') -> str:  # Replace 'UniDic2UDEntry' with your actual type
    line_rows = get_line_rows(entry)
    line_rows = [line[:-2] for line in line_rows]
    return align_tab_separated_values(line_rows, "＿")


def get_line_rows(entry) -> list[list[str]]:
    output = repr(entry)
    return get_lines_from_output(output)


def get_lines_from_output(output:str) -> list[list[str]]:
    output = output.replace("-", "－")  # use a full width character instead to keep the alignment working.
    lines = output.strip().split('\n')  # Split the multiline string into lines
    lines = [line for line in lines if "\t" in line]  # Skip lines that are not the true output
    line_rows = [line.split('\t') for line in lines]  # Split each line by tab and create a list of lists
    for line in line_rows: line.append(line.pop(5))  # move the features line that often differs to the end.
    return line_rows


def align_tab_separated_values(line_rows: list[list[str]], full_width_separator:str = "　") -> str:
    col_widths = [max(len(str(item)) + 2 for item in col) for col in zip(*line_rows)]  # Find the maximum length for each column

    # Determine the type of space for each column
    space_types = []
    for col in zip(*line_rows):
        if all(all(ord(' ') <= ord(c) <= ord('~') for c in item) for item in col):
            space_types.append(' ')  # ASCII characters
        else:
            space_types.append(full_width_separator)  # Japanese full-width space

    aligned_str = '\n'.join(
        ''.join(f"{item + space_types[i] * (col_widths[i] - len(item))}" for i, item in enumerate(row))
        for row in line_rows)

    return aligned_str



# def test_something() -> None:
#     def find_first_index(the_list: list, criteria: callable) -> int:
#         return next((i for i, item in enumerate(the_list) if criteria(item)), -1)
#
#     lst = [1, 4, 7, 10, 13]
#     index = find_first_index(lst, lambda x: x > 500)
#
#     assert index == 2
