from __future__ import annotations

from test_iterable_common import value_test, where_test


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

def test_distinct_removes_duplicates_while_retaining_order() -> None:
    value_test([1, 2, 2, 3, 3],
               lambda x: x.distinct().to_list(),
               [1, 2, 3])

def test_distinct_by_removes_duplicates_by_selected_key_while_retaining_order() -> None:
    value_test([
            ("a", 1),
            ("a", 2),
            ("b", 3),
            ("a", 4),
            ("b", 5)],
            lambda x: x.distinct_by(lambda y: y[0]).to_list(),
            [
                    ("a", 1),
                    ("b", 3)],
            skip_sets=True)
