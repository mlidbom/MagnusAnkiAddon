from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sysutils.collections.linq.l_iterable import LFrozenSet, LIterable, LList, LSet, linq

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

def test_select() -> None:
    select_test((1, 2, 3), lambda x: x * 2, [2, 4, 6])

def test_single_returns_single_value() -> None: value_test([1], lambda x: x.single(), 1)
def test_single_throws_if_no_values() -> None: throws_test([], lambda x: x.single())
def test_single_throws_if_multiple_values() -> None: throws_test([1, 2], lambda x: x.single())

def test_where_first_element() -> None: where_test((1, 2, 3), lambda x: x == 1, [1])
def test_where_middle_element() -> None: where_test((1, 2, 3), lambda x: x == 2, [2])
def test_where_end_element() -> None: where_test((1, 2, 3), lambda x: x == 3, [3])

def test_where_excluding_first_element() -> None: where_test((1, 2, 3), lambda x: x != 1, [2, 3])
def test_where_excluding_middle_element() -> None: where_test((1, 2, 3), lambda x: x != 2, [1, 3])
def test_where_excluding_end_element() -> None: where_test((1, 2, 3), lambda x: x != 3, [1, 2])

def test_to_list() -> None: value_test((1, 2, 3), lambda x: x.to_list(), [1, 2, 3])
def test_to_builtin_list() -> None: value_test((1, 2, 3), lambda x: x.to_built_in_list(), [1, 2, 3])
def test_to_set() -> None: value_test((1, 2, 3), lambda x: x.to_set(), {1, 2, 3})
def test_to_frozenset() -> None: value_test((1, 2, 3), lambda x: x.to_frozenset(), frozenset({1, 2, 3}))

def test_indexer_returns_first_value() -> None: value_test((1, 2, 3), lambda x: x.to_list()[0], 1)
def test_indexer_returns_middle_value() -> None: value_test((1, 2, 3), lambda x: x.to_list()[1], 2)
def test_indexer_returns_last_value() -> None: value_test((1, 2, 3), lambda x: x.to_list()[2], 3)

def test_none_returns_false_if_there_are_elements() -> None: value_test([1], lambda x: x.none(), False)
def test_none_returns_true_if_there_are_no_elements() -> None: value_test([], lambda x: x.none(), True)

def test_not_none_returns_only_elements_that_are_not_none() -> None: value_test([1, None], lambda x: x.not_none().to_list(), [1])
def test_not_none_returns_empty_list_if_all_elements_are_none() -> None: value_test([None, None], lambda x: x.not_none().to_list(), [])

def test_assert_each_throws_if_any_element_does_not_match_predicate() -> None: throws_test([1, 2, 3], lambda x: x.assert_each(lambda y: y != 2), Exception)
def test_assert_each_does_not_throw_if_all_elements_match_predicate() -> None: value_test([1, 2, 3], lambda x: x.assert_each(lambda y: y != 0).to_list(), [1, 2, 3])

def test_for_single_throws_if_there_are_no_elements() -> None:
    def action(x: int) -> None:
        pass
    throws_test([], lambda x: x.for_single(action), Exception)

def test_for_single_throws_if_there_are_multiple_elements() -> None:
    def action(x: int) -> None:
        pass
    throws_test([1,2], lambda x: x.for_single(action), Exception)

def test_for_single_executes_action_if_there_is_exactly_one_element() -> None:
    call_times = 0
    def action(x: int) -> None:
        nonlocal call_times
        call_times += 1

    value_test([1], lambda x: x.for_single(action).to_list(), [1])
    assert call_times == 5


def create_sequences[T](iterable: Iterable[T]) -> list[tuple[str, LIterable[T]]]:
    return [
        ("linq", linq(iterable)),
        ("LList", LList(iterable)),
        ("LSet", LSet(iterable)),
        ("LFRozenSet", LFrozenSet(iterable)),
        ("LIterable.create", LIterable.create(iterable))
    ]

def where_test[TIn, TOut](items: Iterable[TIn],
                          selector: Callable[[TIn], bool],
                          expected_output: list[TOut]) -> None:
    for name, sequence in create_sequences(items):
        result = sequence.where(selector)
        assert result.to_list() == expected_output, name

def select_test[TIn, TOut](items: Iterable[TIn],
                           selector: Callable[[TIn], TOut],
                           expected_output: list[TOut]) -> None:
    for name, sequence in create_sequences(items):
        result = sequence.select(selector)
        assert result.to_list() == expected_output, name

def value_test[TIn, TOut](items: Iterable[TIn],
                          selector: Callable[[LIterable[TIn]], TOut],
                          expected_output: TOut) -> None:
    for name, sequence in create_sequences(items):
        result = selector(sequence)
        assert result == expected_output, name

def throws_test[TIn, TOut](items: Iterable[TIn],
                           selector: Callable[[LIterable[TIn]], TOut],
                           exception_type: type[Exception] = Exception) -> None:
    for name, sequence in create_sequences(items):
        print(name)
        with pytest.raises(exception_type):  # noqa: PT012
            selector(sequence)
            pytest.fail(f"{name}: Expected {exception_type} to be raised")
