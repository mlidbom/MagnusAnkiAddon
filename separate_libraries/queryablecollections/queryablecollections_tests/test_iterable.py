from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.q_iterable import query
from test_iterable_common import CallCounter, select_test, value_test


def test_iterable_can_re_iterate() -> None:
    myquery = query([1, 2, 3]).select(lambda x: x)

    assert myquery.to_list() == [1, 2, 3]
    assert myquery.to_list() == [1, 2, 3]


def test_select() -> None:
    select_test((1, 2, 3), lambda x: x * 2, [2, 4, 6])

def test_to_list() -> None: value_test([1, 2, 3], lambda x: x.to_list(), [1, 2, 3])
def test_to_sequence() -> None: value_test([1, 2, 3], lambda x: x.to_sequence().to_list(), [1, 2, 3])
def test_to_builtin_list() -> None: value_test([1, 2, 3], lambda x: x.to_built_in_list(), [1, 2, 3])
def test_to_set() -> None: value_test([1, 2, 3], lambda x: x.to_set(), {1, 2, 3})
def test_to_frozenset() -> None: value_test([1, 2, 3], lambda x: x.to_frozenset(), frozenset({1, 2, 3}))

def test_concat_appends_second_sequence_to_first() -> None: value_test([1, 2], lambda x: x.concat([3, 4]).to_list(), [1, 2, 3, 4])

def test_any_returns_true_if_there_are_elements() -> None: value_test([1], lambda x: x.any(), True)
def test_any_returns_false_if_there_are_no_elements() -> None: value_test([], lambda x: x.any(), False)

def test_all_returns_true_if_all_elements_match_predicate() -> None: value_test([1, 2, 3], lambda x: x.all(lambda y: y != 0), True)
def test_all_returns_false_if_any_element_does_not_match_predicate() -> None: value_test([1, 2, 3], lambda x: x.all(lambda y: y != 1), False)

def test_none_returns_false_if_there_are_elements() -> None: value_test([1], lambda x: x.none(), False)
def test_none_returns_true_if_there_are_no_elements() -> None: value_test([], lambda x: x.none(), True)

def test_select_many_flattens_nested_sequences() -> None: value_test([[1, 2], [3, 4]], lambda x: x.select_many(lambda y: y).to_list(), [1, 2, 3, 4], skip_sets=True)

def test_reverse_returns_reversed_sequence() -> None: value_test([1, 2, 3], lambda x: x.reversed().to_list(), [3, 2, 1])

def test_not_none_returns_only_elements_that_are_not_none() -> None: value_test([1, None], lambda x: x.where_not_none().to_list(), [1])
def test_not_none_returns_empty_list_if_all_elements_are_none() -> None: value_test(QList[str | None]([None, None]), lambda x: x.where_not_none().to_list(), list[str]())

def test_length_returns_length_of_sequence() -> None:
    value_test([0], lambda x: x.qcount(), 1)
    value_test([0, 3], lambda x: x.qcount(), 2)
    value_test([0, 3, 5], lambda x: x.qcount(), 3)

def test_for_each_executes_action_for_each_element() -> None:
    value_test(lambda: [CallCounter(), CallCounter(), CallCounter()],
               lambda x: x.for_each(lambda y: y.increment()).select(lambda y: y.call_count).to_list(),
               [1, 1, 1])
