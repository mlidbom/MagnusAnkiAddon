from __future__ import annotations

from common_helpers import where_test


def test_where_first_element_returns_only_first_element() -> None:
    where_test((1, 2, 3),
               lambda x: x == 1,
               [1])

def test_where_middle_element_returns_only_middle_element() -> None:
    where_test((1, 2, 3),
               lambda x: x == 2,
               [2])

def test_where_last_element_returns_only_last_element() -> None:
    where_test((1, 2, 3),
               lambda x: x == 3,
               [3])

def test_where_excluding_first_element() -> None:
    where_test((1, 2, 3),
               lambda x: x != 1,
               [2, 3])

def test_where_excluding_middle_element() -> None:
    where_test((1, 2, 3),
               lambda x: x != 2,
               [1, 3])

def test_where_excluding_end_element() -> None:
    where_test((1, 2, 3),
               lambda x: x != 3,
               [1, 2])