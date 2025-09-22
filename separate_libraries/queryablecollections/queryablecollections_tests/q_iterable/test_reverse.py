from __future__ import annotations

from test_common_helpers import value_test


def test_reverse_returns_reversed_sequence() -> None:
    value_test([1, 2, 3],
               lambda x: x.reversed().to_list(),
               [3, 2, 1])
