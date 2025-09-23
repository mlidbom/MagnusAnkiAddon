from __future__ import annotations

from test_common_helpers import value_test_including_unordered_collections


def test_none_returns_false_if_there_are_elements() -> None:
    value_test_including_unordered_collections([1],
                                               lambda x: x.none(),
                                               False)

def test_none_returns_true_if_there_are_no_elements() -> None:
    value_test_including_unordered_collections([],
                                               lambda x: x.none(),
                                               True)
