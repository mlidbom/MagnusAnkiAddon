from __future__ import annotations

from common_helpers import throws_test, value_test


def test_0_returns_element_1() -> None:
    value_test([1, 2, 3],
               lambda x: x.element_at(0),
               1)

def test_1_return_element_2() -> None: value_test(
        [1, 2, 3],
        lambda x: x.element_at(1),
        2)

def test_2_returns_element_3() -> None:
    value_test([1, 2, 3],
               lambda x: x.element_at(2),
               3)

def test_throws_if_index_is_out_of_range() -> None:
    throws_test((1, 2, 3),
                lambda x: x.element_at(3),
                IndexError)