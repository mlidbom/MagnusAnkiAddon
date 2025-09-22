from __future__ import annotations

from common_helpers import value_test


def test_order_by_sorts_in_ascending_order() -> None:
    value_test([3, 2, 1],
               lambda input: input.order_by(lambda y: y).to_list(),
               [1, 2, 3])

def test_order_by_descending_sorts_in_descending_order() -> None:
    value_test([3, 2, 1],
               lambda input: input.order_by_descending(lambda y: y).to_list(),
               [3, 2, 1])

def test_then_by_sorts_in_ascending_order() -> None:
    value_test([3, 2, 1],
               lambda input: input
               .order_by(lambda item: item)
               .then_by(lambda item: item).to_list(),
               [1, 2, 3])

    value_test([3, 2, 1],
               lambda iterable: iterable
               .order_by(lambda item: item)
               .then_by(lambda item: 1 if item == 1 else 0).to_list(),
               [2, 3, 1])

def test_then_by_descending_sorts_in_descending_order() -> None:
    value_test([3, 2, 1],
               lambda x: x.order_by(lambda y: y).then_by_descending(lambda y: y).to_list(), [3, 2, 1])
    value_test([3, 2, 1],
               lambda x: x.order_by(lambda y: y).then_by_descending(lambda y: 1 if y == 2 else 0).to_list(), [2, 1, 3])
