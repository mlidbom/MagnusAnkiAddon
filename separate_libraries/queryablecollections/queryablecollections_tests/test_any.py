from __future__ import annotations

from test_iterable_common import value_test


def test_any_returns_true_if_there_are_elements() -> None: value_test([1], lambda x: x.any(), True)
def test_any_returns_false_if_there_are_no_elements() -> None: value_test([], lambda x: x.any(), False)