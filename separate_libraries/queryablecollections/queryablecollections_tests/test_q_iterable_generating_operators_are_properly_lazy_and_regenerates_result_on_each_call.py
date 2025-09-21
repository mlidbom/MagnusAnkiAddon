from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from queryablecollections.q_iterable import QIterable, query


def assert_has_10_elements[T](iterable: QIterable[T]) -> QIterable[T]:
    assert sum(1 for _ in iterable) == 10
    return iterable

def assert_is_empty[T](iterable: QIterable[T]) -> QIterable[T]:
    assert sum(1 for _ in iterable) == 0
    return iterable

def generate_10_ints() -> QIterable[int]:
    return query(i for i in collection_10_ints())

def collection_10_ints() -> QIterable[int]:
    return query([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

def test_query_can_only_enumerate_once_given_a_generator() -> None:
    generator_query = query(i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert_has_10_elements(generator_query)
    assert_is_empty(generator_query)

def test_query_can_iterate_again_given_a_collection() -> None:
    generator_query = query([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert_has_10_elements(generator_query)
    assert_has_10_elements(generator_query)

type CollectionReturningOperator = Callable[[QIterable[int]], Iterable[object]]
type ScalarOrActionOperator = Callable[[QIterable[int]], Any]
iterator_generating_operators: list[tuple[str, CollectionReturningOperator]] = [
        ("select", lambda x1: x1.select(lambda x2: x2)),
        # ("auto_type", lambda x1: x1.auto_type()), # todo: bug
        ("where", lambda x1: x1.where(lambda x2: True)),
        ("where_not_none", lambda x1: x1.where_not_none()),
        ("distinct", lambda x1: x1.distinct()),
        ("take", lambda x1: x1.take(10)),
        ("take_while", lambda x1: x1.take_while(lambda x2: True)),
        ("take_last", lambda x1: x1.take_last(1)),
        ("skip", lambda x1: x1.skip(1)),
        ("skip_last", lambda x1: x1.skip_last(1)),
        ("of_type", lambda x1: x1.of_type(int)),
        ("order_by", lambda x1: x1.order_by(lambda x2: x2)),
        ("order_by_descending", lambda x1: x1.order_by_descending(lambda x2: x2)),
        ("reversed", lambda x1: x1.reversed())
]

def null_op(_: object) -> None: pass

def swallow_exception_decorator(inner: ScalarOrActionOperator) -> ScalarOrActionOperator:
    def wrapper(argument: QIterable[int]) -> Any:
        try:
            return inner(argument)
        except:
            pass

    return wrapper

scalar_or_action_operators: list[tuple[str, ScalarOrActionOperator]] = [
        ("qcount", lambda x1: x1.qcount()),
        ("none", lambda x1: x1.none()),
        ("any", lambda x1: x1.any()),
        ("all", lambda x1: x1.all(lambda x2: True)),
        ("first", lambda x1: x1.first()),
        ("single", swallow_exception_decorator(lambda x1: x1.single())),
        ("single_or_none", swallow_exception_decorator(lambda x1: x1.single_or_none())),
        ("for_each", lambda x1: x1.for_each(null_op)),
        ("to_list", lambda x1: x1.to_list()),
]

all_tested_operator_names: set[str] = query(iterator_generating_operators).select(lambda x: x[0]).to_set() | query(scalar_or_action_operators).select(lambda x: x[0]).to_set()

def test_all_iterator_generating_operators_when_called_on_generator_backed_iterable_consume_elements() -> None:
    for operator_name, operator in iterator_generating_operators:
        original_iterator = generate_10_ints()
        result = operator(original_iterator)
        original_length = sum(1 for _ in result)
        new_length = sum(1 for _ in result)
        if original_length == 0: raise AssertionError(f"Operator {operator_name} did not return any elements")
        if new_length == original_length: raise AssertionError(f"Operator {operator_name} did not consume any elements")
        if original_iterator.qcount() == 10: raise AssertionError(f"Operator {operator_name} did not consume any from source generator")

def test_no_iterator_generating_operators_when_called_on_collection_backed_iterator_consume_elements() -> None:
    for operator_name, operator in iterator_generating_operators:
        original_iterator = collection_10_ints()
        result_iterator = operator(original_iterator)
        original_length = sum(1 for _ in result_iterator)
        new_length = sum(1 for _ in result_iterator)
        if original_length == 0: raise AssertionError(f"Operator {operator_name} did not return any elements")
        if new_length != original_length: raise AssertionError(f"Operator {operator_name} did consumed elements")
        if original_iterator.qcount() != 10: raise AssertionError(f"Operator {operator_name} mutated source collection")

def test_all_scalar_or_action_operators_when_called_on_generator_backed_iterable_consume_elements() -> None:
    for operator_name, operator in scalar_or_action_operators:
        original_iterator = generate_10_ints()
        operator(original_iterator)
        if original_iterator.qcount() == 10: raise AssertionError(f"Operator {operator_name} consumed no elements")

def test_no_scalar_or_action_operators_when_called_on_collection_backed_iterator_consume_elements() -> None:
    for operator_name, operator in scalar_or_action_operators:
        original_iterator = generate_10_ints()
        operator(original_iterator)
        if original_iterator.qcount() == 10: raise AssertionError(f"Operator {operator_name} mutated source collection")
