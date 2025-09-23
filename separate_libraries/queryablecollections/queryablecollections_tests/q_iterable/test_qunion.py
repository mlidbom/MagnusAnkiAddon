from __future__ import annotations

from test_common_helpers import lists_value_test


def test_combines_distinct_elements_from_both_sequences_preserving_order() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qunion([3, 4, 5]).to_list(),
                     [1, 2, 3, 4, 5])

def test_removes_duplicates_within_first_sequence() -> None:
    lists_value_test([1, 2, 2, 3],
                     lambda x: x.qunion([4, 5]).to_list(),
                     [1, 2, 3, 4, 5])

def test_removes_duplicates_within_second_sequence() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qunion([4, 4, 5]).to_list(),
                     [1, 2, 3, 4, 5])

def test_removes_duplicates_between_sequences() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qunion([2, 3, 4]).to_list(),
                     [1, 2, 3, 4])

def test_with_empty_first_returns_distinct_elements_from_second() -> None:
    lists_value_test([],
                     lambda x: x.qunion([1, 2, 2, 3]).to_list(),
                     [1, 2, 3])

def test_with_empty_second_returns_distinct_elements_from_first() -> None:
    lists_value_test([1, 2, 2, 3],
                     lambda x: x.qunion([]).to_list(),
                     [1, 2, 3])

def test_with_both_empty_returns_empty() -> None:
    lists_value_test([],
                     lambda x: x.qunion([]).to_list(),
                     list[int]())

def test_preserves_order_from_first_sequence_then_second() -> None:
    lists_value_test([3, 1, 2],
                     lambda x: x.qunion([5, 4, 1]).to_list(),
                     [3, 1, 2, 5, 4])

def test_works_with_strings() -> None:
    lists_value_test(["apple", "banana"],
                     lambda x: x.qunion(["banana", "cherry"]).to_list(),
                     ["apple", "banana", "cherry"])

def test_works_with_mixed_types() -> None:
    lists_value_test([1, "hello", 2.5],
                     lambda x: x.qunion([2.5, True, "world"]).to_list(),
                     [1, "hello", 2.5, "world"]) # Note that the True disappears because it is considered equal to 1 in pythn.

def test_with_none_values() -> None:
    lists_value_test([1, None, 2],
                     lambda x: x.qunion([None, 3, 4]).to_list(),
                     [1, None, 2, 3, 4])

def test_with_identical_sequences_returns_distinct_elements() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qunion([1, 2, 3]).to_list(),
                     [1, 2, 3])

def test_with_completely_different_sequences() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qunion([4, 5, 6]).to_list(),
                     [1, 2, 3, 4, 5, 6])

def test_maintains_insertion_order() -> None:
    lists_value_test(["z", "a", "m"],
                     lambda x: x.qunion(["b", "z", "c"]).to_list(),
                     ["z", "a", "m", "b", "c"])

def test_with_single_element_sequences() -> None:
    lists_value_test([42],
                     lambda x: x.qunion([24]).to_list(),
                     [42, 24])

def test_with_duplicate_single_elements() -> None:
    lists_value_test([42],
                     lambda x: x.qunion([42]).to_list(),
                     [42])