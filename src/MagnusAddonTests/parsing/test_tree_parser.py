import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.node import Node


@pytest.mark.parametrize('sentence, excluded, expected', [
    ("知らない", set(), [Node('知らない', '', [Node('知る', '知ら'), Node('ない', '')])]),
    ("いつまでも来ないと知らないからね", {"ないと"}, [Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]), Node('来ないと', '', [Node('来る', '来'), Node('ない', ''), Node('と', '')]), Node('知らない', '', [Node('知る', '知ら'), Node('ない', '')]), Node('から', ''), Node('ね', '')]),
    ("ついに素晴らしい女性に逢えた。", set(), [Node('ついに', ''), Node('素晴らしい', ''), Node('女性', ''), Node('に', ''), Node('逢えた', '', [Node('逢える', '逢え'), Node('た', '')])]), ("ついに素晴らしい女性に逢えた。", {"逢える"}, [Node('ついに', ''), Node('素晴らしい', ''), Node('女性', ''), Node('に', ''), Node('た', '')]),
    ("ううん藤宮さんは日記を捨てるような人じゃない", set(), [Node('ううん', ''), Node('藤宮', ''), Node('さん', ''), Node('は', ''), Node('日記', ''), Node('を', ''), Node('捨てる', ''), Node('ようだ', 'ような', [Node('よう', ''), Node('だ', 'な')]), Node('人', ''), Node('じゃない', '', [Node('じゃ', ''), Node('ない', '')])]),
    ("なかったかな", {"たか", "たかな"}, [Node('なかった','',[Node('ない','なかっ'), Node('た','')]), Node('かな','',[Node('か',''), Node('な','')])]),
    ("探しているんですか", {"探しているんです"}, [Node('探している', '', [Node('探す', '探し'), Node('て', ''), Node('いる', '')]), Node('んです', '', [Node('ん', ''), Node('です', '')]), Node('か', '')]),
    ("としたら", {"とする"}, [Node('とした', 'としたら', [Node('と', ''), Node('した', 'したら', [Node('する', 'し'), Node('た', 'たら')])])]),
    ("離れていくよ", {"いくよ"}, [Node('離れていく', '', [Node('離れる', '離れ'), Node('て', ''), Node('いく', '')]), Node('よ', '')]),
    ("いつまでも来ないと知らないからね", set(), [Node('いつまでも', '', [Node('いつまで', '', [Node('いつ', ''), Node('まで', '')]), Node('も', '')]), Node('来ないと', '', [Node('来る', '来'), Node('ないと', '', [Node('ない', ''), Node('と', '')])]), Node('知らない', '', [Node('知る', '知ら'), Node('ない', '')]), Node('から', ''), Node('ね', '')]),
    ("ダメダメ私を殺して", {"殺し"}, [Node('ダメダメ', ''), Node('私', ''), Node('を', ''), Node('殺して', '', [Node('殺す', '殺し'), Node('て', '')])]),
    ("夢を見た", set(), [Node('夢を見た', '', [Node('夢を見る', '夢を見', [Node('夢', ''), Node('を', ''), Node('見る', '見')]), Node('た', '')])]),
    ("言われるまで気づかなかった", set(), [Node('言われるまで', '', [Node('言う', '言わ'), Node('れる', ''), Node('まで', '')]), Node('気づかなかった', '', [Node('気づく', '気づか'), Node('ない', 'なかっ'), Node('た', '')])]),
    ("行きたい所全部行こう", set(), [Node('行きたい', '', [Node('行く', '行き'), Node('たい', '')]), Node('所', ''), Node('全部', ''), Node('行こう', '', [Node('行く', '行こ'), Node('う', '')])]),
    ("当てられても", set(), [Node('当てられても', '', [Node('当てられる', '当てられ', [Node('当てる', '当て'), Node('られる', 'られ')]), Node('ても', '', [Node('て', ''), Node('も', '')])])]),
    ("食べてもいいけど", set(), [Node('食べてもいいけど', '', [Node('食べる', '食べ'), Node('てもいい', '', [Node('ても', '', [Node('て', ''), Node('も', '')]), Node('いい', '')]), Node('けど', '')])]),
    ("逃げたり", set(), [Node('逃げたり', '', [Node('逃げる', '逃げ'), Node('たり', '')])]),
    ("いるのにキス", {"いるのに"}, [Node('いる', ''), Node('のに', '', [Node('の', ''), Node('に', '')]), Node('キス', '')]),
    ("するためでした", set(), [Node('する', ''), Node('ため', ''), Node('です', 'でし'), Node('た', '')]),
    ("ように言ったのも", {"ように言ったのも", "ように言ったの", "たのも", "たの"}, [Node('ように言った', '', [Node('ように言う', 'ように言っ', [Node('ように', '', [Node('よう', ''), Node('に', '')]), Node('言う', '言っ')]), Node('た', '')]), Node('の', ''), Node('も', '')]),
    ("探しているんですか", {"探しているんです"}, [Node('探している', '', [Node('探す', '探し'), Node('て', ''), Node('いる', '')]), Node('んです', '', [Node('ん', ''), Node('です', '')]), Node('か', '')]),
    ("一度聞いたことがある", set(), [Node('一度', ''), Node('聞いたことがある', '', [Node('聞く', '聞い'), Node('た', ''), Node('ことがある', '', [Node('こと', ''), Node('が', ''), Node('ある', '')])])]),
    ("よかった", set(), [Node('よかった','',[Node('よい','よかっ'), Node('た','')])]),
])
def test_various_stuff(sentence: str, excluded: set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected

@pytest.mark.parametrize('sentence, excluded, expected', [
    ("よかった", set(), [Node('よかった','',[Node('よい','よかっ'), Node('た','')])]),
    ("良ければ", set(), [Node('良ければ','',[Node('良い','良けれ'), Node('ば','')])]),
    ("良かったら", set(), [Node('良かった','良かったら',[Node('良い','良かっ'), Node('た','たら')])]),
    ("良くない", set(), [Node('良くない','',[Node('良い','良く'), Node('ない','')])]),
    ("よかったじゃん", {"よかったじゃん"}, [Node('よかった','',[Node('よい','よかっ'), Node('た','')]), Node('じゃん','')]),
    # adjective within verb compound
    ("言えばよかった", set(), [Node('言えばよかった', '', [Node('言う', '言え'), Node('ば', ''), Node('よかった', '', [Node('よい', 'よかっ'), Node('た', '')])])])
])
def test_adjective_compounds(sentence: str, excluded: set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected

@pytest.mark.parametrize('sentence, excluded, expected', [

])
def test_temp(sentence: str, excluded: set[str], expected: list[Node]) -> None:
    result = tree_parser.parse_tree(sentence, excluded)
    assert result == expected
