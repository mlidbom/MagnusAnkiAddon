from __future__ import annotations

from test_common_helpers import value_test


def test_distinct_removes_duplicates_while_retaining_order() -> None:
    value_test([1, 2, 2, 3, 3],
               lambda x: x.distinct().to_list(),
               [1, 2, 3])