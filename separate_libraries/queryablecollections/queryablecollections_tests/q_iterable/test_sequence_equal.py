from __future__ import annotations

from test_common_helpers import lists_value_test


def test_equal_sequences_return_true() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.sequence_equal([1, 2, 3]),
                     True)

def test_different_order_returns_false() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.sequence_equal([3, 2, 1]),
                     False)

def test_first_longer_returns_false() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.sequence_equal([1, 2]),
                     False)

def test_second_longer_returns_false() -> None:
    lists_value_test([1, 2],
                     lambda x: x.sequence_equal([1, 2, 3]),
                     False)

def test_both_empty_return_true() -> None:
    lists_value_test(list[int](),
                     lambda x: x.sequence_equal([]),
                     True)

def test_single_element_equal_returns_true() -> None:
    lists_value_test([42],
                     lambda x: x.sequence_equal([42]),
                     True)

def test_single_element_different_returns_false() -> None:
    lists_value_test([42],
                     lambda x: x.sequence_equal([24]),
                     False)

def test_with_none_values_compares_positionally() -> None:
    lists_value_test([1, None, 3],
                     lambda x: x.sequence_equal([1, None, 3]),
                     True)

def test_with_none_values_not_equal_when_positions_differ() -> None:
    lists_value_test([None, 1, 3],
                     lambda x: x.sequence_equal([1, None, 3]),
                     False)
