from __future__ import annotations

from test_q_iterable_common import throws_test, value_test


def test_order_by_sorts_in_ascending_order() -> None:
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).to_list(), [1, 2, 3])

def test_order_by_descending_sorts_in_descending_order() -> None:
    value_test([3, 2, 1], lambda x: x.order_by_descending(lambda y: y).to_list(), [3, 2, 1])

def test_then_by_sorts_in_ascending_order() -> None:
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by(lambda y: y).to_list(), [1, 2, 3])
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by(lambda y: 1 if y == 1 else 0).to_list(), [2, 3, 1])

def test_then_by_descending_sorts_in_descending_order() -> None:
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by_descending(lambda y: y).to_list(), [3, 2, 1])
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by_descending(lambda y: 1 if y == 2 else 0).to_list(), [2, 1, 3])

def test_can_sort_ints_implicitly() -> None:
    value_test([3, 2, 1], lambda x: x.ordered().to_list(), [1, 2, 3])

def test_can_sort_strings_implicitly() -> None:
    value_test(["c", "b", "a"], lambda x: x.ordered().to_list(), ["a", "b", "c"])

def test_can_sort_floats_implicitly() -> None:
    value_test([3.0, 2.0, 1.0], lambda x: x.ordered().to_list(), [1.0, 2.0, 3.0])


class MyClass:
    pass

def test_cannot_sort_myclass_implicitly() -> None:
    throws_test([MyClass(), MyClass()], lambda x: x.ordered().to_list(), TypeError)