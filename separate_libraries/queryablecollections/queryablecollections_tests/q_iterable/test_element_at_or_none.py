from __future__ import annotations

from common_helpers import value_test


def test_0_test_returns_element_1() -> None:
    value_test([1, 2, 3],
               lambda x: x.element_at_or_none(0),
               1)

def test_1_return_element_2() -> None:
    value_test([1, 2, 3],
               lambda x: x.element_at_or_none(1),
               2)

def test_2_returns_element_3() -> None:
    value_test([1, 2, 3],
               lambda x: x.element_at_or_none(2),
               3)

def test_returns_none_if_index_is_out_of_range() -> None:
    value_test([1, 2, 3],
               lambda x: x.element_at_or_none(3),
               None)