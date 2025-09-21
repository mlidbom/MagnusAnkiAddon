from __future__ import annotations

from queryablecollections.q_errors import InvalidOperationError
from test_q_iterable_common import throws_test, value_test


def test_single_returns_single_value() -> None: value_test([1], lambda x: x.single(), 1)
def test_single_throws_if_no_values() -> None: throws_test([], lambda x: x.single())
def test_single_throws_if_multiple_values() -> None: throws_test([1, 2], lambda x: x.single())
def test_single_returns_single_none_value() -> None: value_test([None], lambda x: x.single(), None)

def test_single_or_none_returns_single_value() -> None: value_test([1], lambda x: x.single_or_none(), 1)
def test_single_or_none_returns_none_if_no_values() -> None: value_test([], lambda x: x.single_or_none(), None)
def test_single_or_none_throws_if_multiple_values() -> None: throws_test([1, 2], lambda x: x.single_or_none(), InvalidOperationError)

def test_first_returns_first_value() -> None: value_test([1, 2, 3], lambda x: x.first(), 1)
def test_first_throws_if_no_values() -> None: throws_test([], lambda x: x.first())
def test_first_returns_single_none_value() -> None: value_test([None], lambda x: x.first(), None)

def test_first_or_none_returns_first_value() -> None: value_test([1, 2, 3], lambda x: x.first_or_none(), 1)
def test_first_or_none_return_none_if_no_values() -> None: value_test([], lambda x: x.first_or_none(), None)
def test_first_or_none_returns_single_none_value() -> None: value_test([None], lambda x: x.first_or_none(), None)

def test_indexer_returns_first_value() -> None: value_test([1, 2, 3], lambda x: x.to_list()[0], 1)
def test_indexer_returns_middle_value() -> None: value_test([1, 2, 3], lambda x: x.to_list()[1], 2)
def test_indexer_returns_last_value() -> None: value_test([1, 2, 3], lambda x: x.to_list()[2], 3)