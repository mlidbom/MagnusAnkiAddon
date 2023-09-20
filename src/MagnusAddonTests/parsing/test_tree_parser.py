import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node


@pytest.mark.parametrize('sentence, excluded, expected', [
    ("知らない", set(), [Node('知らない','',[Node('知る', '知ら'), Node('ない','')])]),
    ("いつまでも来ないと知らないからね", set(), [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来る', '来'),
        Node('ないと', '', [Node('ない', ''), Node('と', '')]),
        Node('知らない', '', [Node('知る', '知ら'), Node('ない','')]),
        Node('から', ''),
        Node('ね', '')]),
    ("いつまでも来ないと知らないからね", {"ないと"}, [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来る', '来'),
        Node('ない', ''),
        Node('と', ''),
        Node('知らない', '', [Node('知る', '知ら'), Node('ない', '')]),
        Node('から', ''),
        Node('ね', '')]),
    ("ついに素晴らしい女性に逢えた。", set(), [
        Node('ついに',''),
        Node('素晴らしい',''),
        Node('女性',''),
        Node('に',''),
        Node('逢える', '逢え'),
        Node('た', '')]),
    ("ついに素晴らしい女性に逢えた。", {"逢える"}, [
        Node('ついに', ''),
        Node('素晴らしい', ''),
        Node('女性', ''),
        Node('に', ''),
        Node('た','')]),
    ("ううん藤宮さんは日記を捨てるような人じゃない", set(),[
        Node('ううん',''),
        Node('藤宮',''),
        Node('さん',''),
        Node('は',''),
        Node('日記',''),
        Node('を',''),
        Node('捨てる',''),
        Node('ようだ','ような',[Node('よう',''), Node('だ','な')]),
        Node('人',''),
        Node('じゃ',''),
        Node('ない','')])
])
def test_stuff(sentence: str, excluded:set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected

@pytest.mark.parametrize('sentence, excluded, expected', [
    ("なかったかな", {"たか"}, [])
])
def test_temp(sentence: str, excluded:set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected