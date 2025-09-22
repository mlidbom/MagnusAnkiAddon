from __future__ import annotations

from common_helpers import value_test


def test_none_returns_false_if_there_are_elements() -> None:
    value_test([1],
               lambda x: x.none(),
               False)

def test_none_returns_true_if_there_are_no_elements() -> None:
    value_test([],
               lambda x: x.none(),
               True)
