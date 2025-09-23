from __future__ import annotations

from queryablecollections.q_errors import EmptyIterableError
from test_common_helpers import throws_test, value_test_including_unordered_collections


def test_returns_last_value() -> None:
    value_test_including_unordered_collections([1, 2, 3],
                                               lambda x: x.last(),
                                               3)

def test_returns_single_none_value() -> None:
    value_test_including_unordered_collections([None],
                                               lambda x: x.last(),
                                               None)

def test_with_predicate_returns_last_matching_value() -> None:
    value_test_including_unordered_collections([1, 2, 3, 4, 5],
                                               lambda x: x.last(lambda y: y < 5),
                                               4)

def test_with_predicate_raises_if_no_match() -> None:
    throws_test([1, 3, 5],
                lambda x: x.last(lambda y: y > 5),
                EmptyIterableError)

def test_throws_if_no_values() -> None:
    throws_test([],
                lambda x: x.last(),
                EmptyIterableError)

def test_throws_if_no_match_for_predicate() -> None:
    throws_test([1, 3, 5],
                lambda x: x.last(lambda y: y % 2 == 0),
                EmptyIterableError)
