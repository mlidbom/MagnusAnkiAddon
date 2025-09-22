from __future__ import annotations

from test_common_helpers import value_test


def test_returns_true_if_all_elements_match_predicate() -> None:
    value_test([1, 2, 3],
               lambda x: x.all(lambda y: y != 0),
               True)

def test_eturns_false_if_any_element_does_not_match_predicate() -> None:
    value_test([1, 2, 3],
               lambda x: x.all(lambda y: y != 1),
               False)
