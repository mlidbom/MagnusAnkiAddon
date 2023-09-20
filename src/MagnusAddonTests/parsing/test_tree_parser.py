import pytest

from parsing.tree_parsing import tree_parser


@pytest.mark.parametrize('sentence', [
    "いつまでも来ないと知らないからね"
])
def test_draft(sentence: str) -> None:
    result = tree_parser.parse_tree(sentence)
    for something in result:
        print(something)


