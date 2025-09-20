from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_sequence import QImmutableSequence


def test_list_slice_from_start_returns_the_specified_slice() -> None:
    assert QList((1, 2, 3, 4, 5, 6, 7))[:2] == QList([1, 2])

def test_sequence_slice_from_start_returns_the_specified_slice() -> None:
    assert QImmutableSequence((1, 2, 3, 4, 5, 6, 7))[:2].to_list() == QList([1, 2])

def test_list_slice_middle__returns_the_specified_slice() -> None:
    assert QList((1, 2, 3, 4, 5))[2:4] == QList([3, 4])

def test_sequence_slice_middle_returns_the_specified_slice() -> None:
    assert QImmutableSequence((1, 2, 3, 4, 5))[2:4].to_list() == QList([3, 4])

def test_list_slice_end_returns_the_specified_slice() -> None:
    assert QList((1, 2, 3, 4, 5))[3:] == QList([4, 5])

def test_sequence_slice_end_returns_the_specified_slice() -> None:
    assert QImmutableSequence((1, 2, 3, 4, 5))[3:].to_list() == QList([4, 5])

def test_list_slice_returns_qlist() -> None:
    value = QList((1, 2, 3))[1:]
    assert isinstance(value, QList)
    assert value.element_at(0) == 2

def test_sequence_slice_returns_qimmutable_sequence() -> None:
    value = QImmutableSequence((1, 2, 3))[1:]
    assert isinstance(value, QImmutableSequence)
    assert value.element_at(0) == 2

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