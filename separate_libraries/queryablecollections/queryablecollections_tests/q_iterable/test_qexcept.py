from __future__ import annotations

from test_common_helpers import lists_value_test


def test_removes_elements_present_in_other_collection_without_changing_the_order() -> None:
    lists_value_test([1, 2, 3, 4, 5],
                     lambda x: x.qexcept([3, 4, 6, 7]).to_list(),
                     [1, 2, 5])

def test_removes_duplicates_from_result() -> None:
    lists_value_test([1, 2, 2, 3, 3, 4],
                     lambda x: x.qexcept([3, 4]).to_list(),
                     [1, 2])

def test_with_empty_other_returns_distinct_elements_from_first() -> None:
    lists_value_test([1, 2, 2, 3],
                     lambda x: x.qexcept([]).to_list(),
                     [1, 2, 3])

def test_with_empty_first_returns_empty() -> None:
    lists_value_test([],
                     lambda x: x.qexcept([1, 2, 3]).to_list(),
                     list[int]())

def test_with_no_matching_elements_returns_distinct_elements_from_first() -> None:
    lists_value_test([1, 2, 3, 3],
                     lambda x: x.qexcept([4, 5, 6]).to_list(),
                     [1, 2, 3])

def test_with_all_matching_elements_returns_empty() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qexcept([1, 2, 3, 4]).to_list(),
                     list[int]())

def test_works_with_strings() -> None:
    lists_value_test(["apple", "banana", "cherry", "date"],
                     lambda x: x.qexcept(["banana", "date", "elderberry"]).to_list(),
                     ["apple", "cherry"])

def test_works_with_bool_types() -> None:
    lists_value_test([True, False, True, False],
                     lambda x: x.qexcept([False]).to_list(),
                     [True])

def test_works_with_mixed_types() -> None:
    lists_value_test([1, "hello", 2.5, True, None, False, 0],
                     lambda x: x.qexcept(["hello", 2.5, False]).to_list(),
                     [1, None]) #note, python considers 1 and True to be equal and False and 0 to be equal, that's why the True, and the 0 are gone. It's not a bug in this implementation, it's unfixable in python.

def test_with_none_values() -> None:
    lists_value_test([1, None, 2, None, 3],
                     lambda x: x.qexcept([None, 2]).to_list(),
                     [1, 3])

def test_with_none_values_retain_none_values_unless_excluded() -> None:
    lists_value_test([1, None, 2, None, 3],
                     lambda x: x.qexcept([2]).to_list(),
                     [1, None, 3])