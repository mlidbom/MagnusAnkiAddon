import pytest

from language_services.janome_ex.tree_building import tree_parser
from language_services.janome_ex.tree_building.tree_parser_node import TreeParserNode, priorities

p = priorities


@pytest.mark.parametrize('sentence, expected_priorities', [
    ("言われるまで気づかなかった", {
        'た': 'very_low',
        'なかっ': 'medium',
        'まで': 'low',
        'れる': 'low',
        '気づか': 'medium',
        '気づかなかった': 'medium',
        '言わ': 'medium',
        '言われるまで': 'medium'}),
    ("いつまでも来ないと知らないからね", {
        'いつ': 'low',
        'いつまで': 'medium',
        'いつまでも': 'medium',
        'から': 'low',
        'と': 'very_low',
        'ない': 'low',
        'ないと': 'medium',
        'ね': 'very_low',
        'まで': 'low',
        'も': 'very_low',
        '来': 'medium',
        '来ないと': 'medium',
        '知ら': 'medium',
        '知らない': 'medium'}),
    ("日記", {'日記': 'high'})
])
def test_priorities(sentence: str, expected_priorities: dict[str, str]) -> None:
    real_priorities: dict[str, str] = dict()

    def register_priority(own_node: TreeParserNode) -> None:
        real_priorities[own_node.surface] = own_node.get_priority_class(own_node.surface, set())

    result = tree_parser.parse_tree(sentence, set())
    result.visit(register_priority)

    assert real_priorities == expected_priorities
