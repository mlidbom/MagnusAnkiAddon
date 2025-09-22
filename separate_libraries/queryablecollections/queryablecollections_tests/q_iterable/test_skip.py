from __future__ import annotations

from queryablecollections.q_iterable import query


def test_skip_skips_the_specified_number_of_elements() -> None:
    assert query([1, 2, 3, 4, 5]).skip(2).to_list() == [3, 4, 5]

def test_skip_zero_returns_all_elements() -> None:
    assert query([1, 2, 3, 4, 5]).skip(0).to_list() == [1, 2, 3, 4, 5]

def test_skip_negative_count_returns_all_elements() -> None:
    assert query([1, 2, 3, 4, 5]).skip(-3).to_list() == [1, 2, 3, 4, 5]

def test_skip_more_than_available_returns_no_elements() -> None:
    assert query([1, 2, 3]).skip(10).to_list() == []

def test_skip_from_empty_returns_no_elements() -> None:
    assert query([]).skip(5).to_list() == []
