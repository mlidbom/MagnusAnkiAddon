from __future__ import annotations

from test_iterable_common import value_test


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
