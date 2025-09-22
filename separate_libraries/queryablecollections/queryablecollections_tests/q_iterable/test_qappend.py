from __future__ import annotations

from test_common_helpers import lists_value_test


def test_adds_single_element_to_end() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qappend(4).to_list(),
                     [1, 2, 3, 4])

def test_to_empty_collection_returns_single_element() -> None:
    lists_value_test([],
                     lambda x: x.qappend(42).to_list(),
                     [42])

def test_works_with_none_value() -> None:
    lists_value_test([1, None, 3],
                     lambda x: x.qappend(None).to_list(),
                     [1, None, 3, None])

def test_different_type_to_mixed_collection() -> None:
    lists_value_test([1, "hello", 3.14],
                     lambda x: x.qappend(True).to_list(),
                     [1, "hello", 3.14, True])

def test_multiple_appends_chain_correctly() -> None:
    lists_value_test([1, 2],
                     lambda x: x.qappend(3).qappend(4).qappend(5).to_list(),
                     [1, 2, 3, 4, 5])

def test_works_with_single_element_collection() -> None:
    lists_value_test([42],
                     lambda x: x.qappend(24).to_list(),
                     [42, 24])
