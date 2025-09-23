from __future__ import annotations

from test_common_helpers import value_test


def test_returns_tuple_of_index_and_item() -> None:
    value_test([10, 20, 30],
               lambda x: x.qindex().to_list(),
               [(0, 10), (1, 20), (2, 30)],
               skip_sets=True)

def test_with_empty_collection_returns_empty() -> None:
    value_test(list[int](),
               lambda x: x.qindex().to_list(),
               list[tuple[int, int]](),
               skip_sets=True)
