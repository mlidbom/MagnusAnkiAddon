from __future__ import annotations

from common_helpers import throws_test, value_test


def test_first_returns_first_value() -> None: value_test([1, 2, 3], lambda x: x.first(), 1)
def test_first_throws_if_no_values() -> None: throws_test([], lambda x: x.first())
def test_first_returns_single_none_value() -> None: value_test([None], lambda x: x.first(), None)

def test_first_or_none_returns_first_value() -> None: value_test([1, 2, 3], lambda x: x.first_or_none(), 1)
def test_first_or_none_return_none_if_no_values() -> None: value_test([], lambda x: x.first_or_none(), None)
def test_first_or_none_returns_single_none_value() -> None: value_test([None], lambda x: x.first_or_none(), None)
