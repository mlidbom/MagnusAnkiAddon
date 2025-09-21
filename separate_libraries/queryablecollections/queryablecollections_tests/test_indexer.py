from __future__ import annotations

from test_iterable_common import value_test


def test_indexer_returns_first_value() -> None:
    value_test([1, 2, 3],
               lambda x: x.to_list()[0],
               1)

def test_indexer_returns_middle_value() -> None:
    value_test([1, 2, 3],
               lambda x: x.to_list()[1],
               2)

def test_indexer_returns_last_value() -> None:
    value_test([1, 2, 3],
               lambda x: x.to_list()[2],
               3)
