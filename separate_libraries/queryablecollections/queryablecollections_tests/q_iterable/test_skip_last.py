from __future__ import annotations

from queryablecollections.q_iterable import query


def test_skip_last_skips_the_last_x_elements() -> None:
    assert query([1, 2, 3, 4, 5]).skip_last(2).to_list() == [1, 2, 3]

def test_skip_last_zero_returns_all_elements() -> None:
    assert query([1, 2, 3, 4, 5]).skip_last(0).to_list() == [1, 2, 3, 4, 5]

def test_skip_last_negative_returns_all_elements() -> None:
    assert query([1, 2, 3, 4, 5]).skip_last(-3).to_list() == [1, 2, 3, 4, 5]

def test_skip_last_more_than_available_returns_no_elements() -> None:
    assert query([1, 2, 3]).skip_last(10).to_list() == []

def test_skip_last_from_empty_returns_no_elements() -> None:
    assert query([]).skip_last(5).to_list() == []

def test_skip_last_single_element_returns_no_elements() -> None:
    assert query([42]).skip_last(1).to_list() == []