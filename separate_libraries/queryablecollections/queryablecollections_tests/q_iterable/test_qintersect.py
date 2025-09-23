from __future__ import annotations

from test_common_helpers import lists_value_test


def test_returns_common_elements_preserving_first_order_and_distinct() -> None:
    lists_value_test([1, 2, 2, 3, 4, 5],
                     lambda x: x.qintersect([2, 3, 6, 2]).to_list(),
                     [2, 3])

def test_returns_common_elements_preserving_first_order_and_distinct_another_verification_of_order_since_we_seem_to_have_some_issue() -> None:
    lists_value_test([5, 4, 3, 2, 1],
                     lambda x: x.qintersect([1, 2, 3, 4, 5]).to_list(),
                     [5, 4, 3, 2, 1])

def test_with_empty_first_returns_empty() -> None:
    lists_value_test([],
                     lambda x: x.qintersect([1, 2, 3]).to_list(),
                     list[int]())

def test_with_empty_second_returns_empty() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qintersect([]).to_list(),
                     list[int]())

def test_with_no_common_elements_returns_empty() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.qintersect([4, 5, 6]).to_list(),
                     list[int]())

def test_with_strings() -> None:
    lists_value_test(["apple", "banana", "cherry", "banana"],
                     lambda x: x.qintersect(["banana", "date"]).to_list(),
                     ["banana"])

def test_with_mixed_types() -> None:
    lists_value_test([1, "hello", 2.5, True, None, False, 0],
                     # since in python True equals 1 and False equals 0 we cannot reliably assert using any of True, False, 1, 0, so we get to convert to strings to see what is actually happening....
                     lambda x: x.qintersect([True, "hello", 3.14, 0, False]).select(str).to_list(),
                     ["1", "hello", "False"])

def test_with_none_values() -> None:
    lists_value_test([1, None, 2, None, 3],
                     lambda x: x.qintersect([None, 2]).to_list(),
                     [None, 2])  # Note: True equals 1 in Python and False equals 0. Thus this assertion and the one adev are equivalent.
