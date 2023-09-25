import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.tree_parser_node import TreeParserNode, priorities

p = priorities


@pytest.mark.parametrize('sentence, expected_priorities', [
    ("言われるまで気づかなかった", {
        'た': 'very_low',
        'ない': 'low',
        'まで': 'low',
        'れる': 'low',
        '気づかなかった': 'medium',
        '気づく': 'medium',
        '言う': 'medium',
        '言われるまで': 'medium'}),
    ("いつまでも来ないと知らないからね", {
        'も': 'very_low',
        'と': 'very_low',
        'から': 'low',
        'ない': 'low',
        'まで': 'low',
        'いつ': 'low',
        'いつまで': 'medium',
        'いつまでも': 'medium',
        'ないと': 'medium',
        '来ないと': 'medium',
        '来る': 'medium',
        '知らない': 'medium',
        '知る': 'medium',
        'ね': 'very_low'}),
    ("日記", {'日記': 'high'})
])
def test_priorities(sentence: str, expected_priorities: dict[str, str]) -> None:
    real_priorities: dict[str, str] = dict()

    def register_priority(own_node: TreeParserNode):
        real_priorities[own_node.base] = own_node.get_priority_class(own_node.base)

    result = tree_parser.parse_tree(sentence, set())
    result.visit(register_priority)

    assert real_priorities == expected_priorities
