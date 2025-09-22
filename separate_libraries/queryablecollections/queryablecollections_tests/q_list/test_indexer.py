from __future__ import annotations

from queryablecollections.collections.q_immutable_sequence import QImmutableSequence
from queryablecollections.collections.q_list import QList


def test_list_indexer_returns_element_at_index() -> None:
    values = QList((0, 1, 2))
    assert values[0] == 0
    assert values[1] == 1
    assert values[2] == 2

def test_sequence_indexer_returns_element_at_index() -> None:
    values = QImmutableSequence((0, 1, 2))
    assert values[0] == 0
    assert values[1] == 1
    assert values[2] == 2