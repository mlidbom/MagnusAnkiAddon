from __future__ import annotations

from common_helpers import lists_value_test


def test_adds_single_element_to_beginning() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.prepend(0).to_list(),
                     [0, 1, 2, 3])

def test_to_empty_collection_returns_single_element() -> None:
    lists_value_test([],
                     lambda x: x.prepend(42).to_list(),
                     [42])

def test_works_with_none_value() -> None:
    lists_value_test([1, None, 3],
                     lambda x: x.prepend(None).to_list(),
                     [None, 1, None, 3])

def test_different_type_to_mixed_collection() -> None:
    lists_value_test([1, "hello", 3.14],
                     lambda x: x.prepend(True).to_list(),
                     [True, 1, "hello", 3.14])

def test_multiple_prepends_chain_correctly() -> None:
    lists_value_test([3, 4],
                     lambda x: x.prepend(2).prepend(1).prepend(0).to_list(),
                     [0, 1, 2, 3, 4])

def test_works_with_single_element_collection() -> None:
    lists_value_test([42],
                     lambda x: x.prepend(24).to_list(),
                     [24, 42])

def test_prepend_and_append_work_together() -> None:
    lists_value_test([2, 3],
                     lambda x: x.prepend(1).qappend(4).to_list(),
                     [1, 2, 3, 4])

def test_preserves_order_with_strings() -> None:
    lists_value_test(["world"],
                     lambda x: x.prepend("hello").to_list(),
                     ["hello", "world"])

def test_works_with_duplicate_values() -> None:
    lists_value_test([1, 2, 1],
                     lambda x: x.prepend(1).to_list(),
                     [1, 1, 2, 1])