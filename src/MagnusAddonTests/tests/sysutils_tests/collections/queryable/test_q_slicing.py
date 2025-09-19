from __future__ import annotations

from sysutils.collections.linq.q_iterable import QList


def test_list_slice_from_start() -> None:
    assert QList((1, 2, 3, 4, 5, 6, 7))[:2] == QList([1, 2])

def test_list_slice_middle() -> None:
    assert QList((1, 2, 3, 4, 5))[2:4] == QList([3, 4])

def test_list_slice_end() -> None:
    assert QList((1, 2, 3, 4, 5))[3:] == QList([4, 5])

def test_list_slice_returns_qlist() -> None:
    value = QList((1, 2, 3))[1:]
    assert isinstance(value, QList)
    assert value.element_at(0) == 2

def test_list_index_returns_element_at_index() -> None:
    values = QList((0, 1, 2))
    assert values[0] == 0
    assert values[1] == 1
    assert values[2] == 2