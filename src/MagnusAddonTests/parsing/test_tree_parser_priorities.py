import pytest

from parsing.tree_parsing import tree_parser
from parsing.tree_parsing.parse_tree_node import Node, priorities

p = priorities


@pytest.mark.parametrize('sentence, expected_priorities', [
    ("言われるまで気づかなかった", {
        'た': 'low',
        'ない': 'low',
        'まで': 'low',
        'れる': 'low',
        '気づかなかった': 'medium',
        '気づく': 'medium',
        '言う': 'medium',
        '言われるまで': 'medium'}),
    ("いつまでも来ないと知らないからね", {
        'いつ': 'medium',
        'いつまで': 'medium',
        'いつまでも': 'medium',
        'ないと': 'medium',
        '来ないと': 'medium',
        '来る': 'medium',
        '知らない': 'medium',
        '知る': 'medium',
        'ね': 'medium',
        'から': 'low',
        'と': 'low',
        'ない': 'low',
        'まで': 'low',
        'も': 'low'})
])
def test_priorities(sentence: str, expected_priorities: dict[str, str]) -> None:
    real_priorities: dict[str, str] = dict()

    def register_priority(own_node: Node):
        real_priorities[own_node.base] = own_node.get_priority_class(own_node.base)

    result = tree_parser.parse_tree(sentence, set())
    for node in result:
        node.visit(register_priority)

    assert real_priorities == expected_priorities
