# tests/test_contains.py
from __future__ import annotations

from queryablecollections.q_iterable import query


def test_true_for_present_value() -> None:
    data = query([1, 2, 3, 4])
    assert data.contains(3) is True

def test_false_for_absent_value() -> None:
    data = query([1, 2, 3, 4])
    assert data.contains(5) is False

def test_contains_after_filtering() -> None:
    data = query([1, 2, 3, 4, 5]).where(lambda x: x % 2 == 0)
    assert data.contains(2) is True
    assert data.contains(1) is False

def test_contains_with_custom_equality_like_tuples() -> None:
    items = query([("a", 1), ("b", 2)])
    assert items.contains(("a", 1)) is True
    assert items.contains(("a", 2)) is False

def test_contains_for_iterable_without_fast_membership() -> None:
    # Use a generator to ensure fallback to iteration works
    gen_data = query(x for x in range(5))
    assert gen_data.contains(4) is True
    assert gen_data.contains(10) is False
