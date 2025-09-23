from __future__ import annotations

from test_common_helpers import value_test_including_unordered_collections


def test_returns_last_value() -> None:
    value_test_including_unordered_collections([1, 2, 3],
                                               lambda x: x.last_or_none(),
                                               3)

def test_return_none_if_no_values() -> None:
    value_test_including_unordered_collections([],
                                               lambda x: x.last_or_none(),
                                               None)

def test_returns_none_when_no_match_to_predicate() -> None:
    value_test_including_unordered_collections([1, 3, 5],
                                               lambda x: x.last_or_none(lambda y: y % 2 == 0),
                                               None)
