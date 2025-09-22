from __future__ import annotations

from queryablecollections.q_iterable import query


def test_take_last_returns_the_last_x_elements() -> None:
    assert query([1, 2, 3, 4, 5]).take_last(3).to_list() == [3, 4, 5]

def test_take_last_zero_returns_no_elements() -> None:
    assert query([1, 2, 3, 4, 5]).take_last(0).to_list() == []

def test_take_last_negative_count_returns_no_elements() -> None:
    assert query([1, 2, 3, 4, 5]).take_last(-5).to_list() == []

def test_take_last_more_than_available_returns_all_elements() -> None:
    assert query([1, 2, 3]).take_last(10).to_list() == [1, 2, 3]

def test_take_last_from_empty_returns_no_elements() -> None:
    assert query([]).take_last(5).to_list() == []

def test_take_last_single_element_returns_the_single_element() -> None:
    assert query([42]).take_last(1).to_list() == [42]