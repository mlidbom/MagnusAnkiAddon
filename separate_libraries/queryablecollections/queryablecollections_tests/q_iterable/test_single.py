from __future__ import annotations

from test_common_helpers import throws_test, value_test


def test_single_returns_single_value() -> None:
    value_test([1],
               lambda x: x.single(),
               1)

def test_single_throws_if_no_values() -> None:
    throws_test([],
                lambda x: x.single())

def test_single_throws_if_multiple_values() -> None:
    throws_test([1, 2],
                lambda x: x.single())

def test_single_returns_single_none_value() -> None:
    value_test([None],
               lambda x: x.single(),
               None)
