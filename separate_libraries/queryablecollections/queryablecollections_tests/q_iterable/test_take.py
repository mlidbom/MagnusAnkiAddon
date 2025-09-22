from __future__ import annotations

from queryablecollections.q_iterable import query


def test_take_returns_the_specified_number_of_elements_from_the_start() -> None:
    assert query([1, 2, 3, 4, 5]).take(3).to_list() == [1, 2, 3]

def test_take_zero_returns_empty_iterable() -> None:
    assert query([1, 2, 3, 4, 5]).take(0).to_list() == []

def test_take_negative_returns_empty_iterable() -> None:
    assert query([1, 2, 3, 4, 5]).take(-5).to_list() == []

def test_take_more_than_available_returns_the_full_iterable() -> None:
    assert query([1, 2, 3]).take(10).to_list() == [1, 2, 3]

def test_take_from_empty_returns_empty_iterable() -> None:
    assert query([]).take(5).to_list() == []