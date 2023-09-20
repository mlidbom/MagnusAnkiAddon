import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node


@pytest.mark.parametrize('sentence, excluded, expected', [
    ("知らない", set(), [Node('知らない','',[Node('知ら','知る'), Node('ない','')])]),
    ("いつまでも来ないと知らないからね", set(), [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来', '来る'),
        Node('ないと', '', [Node('ない', ''), Node('と', '')]),
        Node('知らない', '', [Node('知ら', '知る'), Node('ない','')]),
        Node('から', ''),
        Node('ね', '')]),
    ("いつまでも来ないと知らないからね", {"ないと"}, [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来', '来る'),
        Node('ない', ''),
        Node('と', ''),
        Node('知らない', '', [Node('知ら', '知る'), Node('ない', '')]),
        Node('から', ''),
        Node('ね', '')]),
    ("ついに素晴らしい女性に逢えた。", set(), [
        Node('ついに',''),
        Node('素晴らしい',''),
        Node('女性',''),
        Node('に',''),
        Node('逢え','逢える')]),
    ("ついに素晴らしい女性に逢えた。", {"逢える"}, [
        Node('ついに', ''),
        Node('素晴らしい', ''),
        Node('女性', ''),
        Node('に', '')])
])
def test_draft(sentence: str, excluded:set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected
