import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node


@pytest.mark.parametrize('sentence, expected', [
    ("知らない", [Node('知らない','',[Node('知ら','知る'), Node('ない','')])]),
    ("いつまでも来ないと知らないからね", [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来', '来る'),
        Node('ないと', '', [Node('ない', ''), Node('と', '')]),
        Node('知らない', '', [Node('知ら', '知る'), Node('ない','')]),
        Node('から', ''),
        Node('ね', '')])
])
def test_draft(sentence: str, expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence)
    assert result == expected
