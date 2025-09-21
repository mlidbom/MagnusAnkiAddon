from __future__ import annotations

from test_iterable_common import throws_test, value_test


def test_element_at_returns_first_element() -> None: value_test([1, 2, 3], lambda x: x.element_at(0), 1)
def test_element_at_return_middle_element() -> None: value_test([1, 2, 3], lambda x: x.element_at(1), 2)
def test_element_at_returns_last_element() -> None: value_test([1, 2, 3], lambda x: x.element_at(2), 3)
def test_element_at_throws_if_index_is_out_of_range() -> None: throws_test((1, 2, 3), lambda x: x.element_at(3), IndexError)
def test_element_at_after_to_list_throws_if_index_is_out_of_range() -> None: throws_test((1, 2, 3), lambda x: x.element_at(3), IndexError)

def test_element_at_or_none_returns_first_element() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(0), 1)
def test_element_at_or_none_return_middle_element() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(1), 2)
def test_element_at_or_none_returns_last_element() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(2), 3)
def test_element_at_or_none_returns_none_if_index_is_out_of_range() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(3), None)
def test_element_at_or_none_after_to_list_returns_none_if_index_is_out_of_range() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(3), None)