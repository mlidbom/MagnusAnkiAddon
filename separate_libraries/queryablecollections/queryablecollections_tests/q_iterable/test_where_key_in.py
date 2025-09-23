from __future__ import annotations

from test_common_helpers import lists_value_test


def test_returns_common_elements_by_key_preserving_first_order_and_distinct_by_key() -> None:
    lists_value_test([("a", 1), ("b", 2), ("a", 3), ("c", 4), ("b", 5)],
                     lambda x: x.where_key_in(["c", "a"], lambda item: item[0]).to_list(),
                     [("a", 1), ("c", 4)])

def test_intersect_by_with_empty_first_returns_empty() -> None:
    lists_value_test([],
                     lambda x: x.where_key_in(["a", "b"], lambda item: item).to_list(),
                     list[str]())

def test_intersect_by_with_empty_keys_returns_empty() -> None:
    lists_value_test([("a", 1), ("b", 2)],
                     lambda x: x.where_key_in([], lambda item: item[0]).to_list(),
                     list[tuple[str, int]]())

def test_intersect_by_with_no_common_keys_returns_empty() -> None:
    lists_value_test([("a", 1), ("b", 2)],
                     lambda x: x.where_key_in(["x", "y"], lambda item: item[0]).to_list(),
                     list[tuple[str, int]]())

def test_intersect_by_handles_none_keys() -> None:
    lists_value_test([("a", 1), (None, 2), ("b", 3), (None, 4)],
                     lambda x: x.where_key_in([None], lambda item: item[0]).to_list(),
                     [(None, 2)])

def test_intersect_by_duplicate_keys_in_second_do_not_affect_result() -> None:
    lists_value_test([(1, "x"), (2, "y"), (3, "z"), (2, "y2")],
                     lambda x: x.where_key_in([2, 2, 3], lambda item: item[0]).to_list(),
                     [(2, "y"), (3, "z")])
