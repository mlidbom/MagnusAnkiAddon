from __future__ import annotations

import pytest
from queryablecollections.q_errors import EmptyIterableError
from test_common_helpers import lists_value_test, throws_test


def test_max_by_returns_item_with_largest_key() -> None:
    lists_value_test(
        ["apple", "banana", "cherry", "fig"],
        lambda x: x.max_by(len),
        "banana"  # "banana" and "cherry" have len 6, first wins
    )

def test_max_by_raises_on_empty() -> None:
    with pytest.raises(EmptyIterableError):
        lists_value_test(list[str](), lambda x: x.max_by(len), None)  # value ignored due to exception


def test_max_by_with_ties_returns_first_encountered() -> None:
    lists_value_test(
        ["aa", "bbb", "cc", "ddd", "e"],
        lambda x: x.max_by(len),
        "bbb"  # len 3 tie with "ddd", first wins
    )

def test_raises_type_error_if_selector_returns_non_comparable() -> None:
    class NonComparable:
        def __init__(self, value: str) -> None:
            self.value = value

    throws_test(
            ["a", "b", "c"],
            lambda x: x.max_by(lambda y: NonComparable(y)),  # pyright: ignore [reportArgumentType]
            TypeError
    )
