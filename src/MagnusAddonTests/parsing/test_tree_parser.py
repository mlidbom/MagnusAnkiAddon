import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node


@pytest.mark.parametrize('sentence, excluded, expected', [
    ("知らない", set(), [Node('知らない','',[Node('知る', '知ら'), Node('ない','')])]),
    ("いつまでも来ないと知らないからね", {"ないと"}, [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来ないと', '', [Node('来る', '来'), Node('ない', ''), Node('と', '')]),
        Node('知らない', '', [Node('知る', '知ら'), Node('ない', '')]),
        Node('から', ''),
        Node('ね', '')]),
    ("ついに素晴らしい女性に逢えた。", set(), [
        Node('ついに', ''),
        Node('素晴らしい', ''),
        Node('女性', ''),
        Node('に', ''),
        Node('逢えた', '', [Node('逢える', '逢え'), Node('た', '')])]),
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
        Node('じゃない','',[Node('じゃ',''), Node('ない','')])]),
    ("なかったかな", {"たか", "たかな"}, [
        Node('ない','なかっ'),
        Node('た',''),
        Node('かな','',[Node('か',''), Node('な','')])]),
    ("探しているんですか", set(), [
        Node('探しているんです', '', [Node('探す', '探し'), Node('て', ''), Node('いる', ''), Node('んです', '', [Node('ん', ''), Node('です', '')])]),
        Node('か', '')
    ]),
    ("としたら", {"とする"}, [Node('とした','としたら',[Node('と',''), Node('した','したら',[Node('する','し'), Node('た','たら')])])]),
    ("離れていくよ", set(), [
        Node('離れていく', '', [Node('離れる', '離れ'), Node('て', ''), Node('いく', '')]), Node('よ', '')])
])
def test_stuff(sentence: str, excluded:set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected

@pytest.mark.parametrize('sentence, excluded, expected', [
    ("いつまでも来ないと知らないからね", set(), [
        Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]),
        Node('来ないと', '', [Node('来る', '来'), Node('ないと', '', [Node('ない', ''), Node('と', '')])]),
        Node('知らない', '', [Node('知る', '知ら'), Node('ない', '')]),
        Node('から', ''),
        Node('ね', '')]),
])
def test_temp(sentence: str, excluded:set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    something = 1
    assert result == expected