
from __future__ import annotations

from queryablecollections.collections.q_list import QList
from queryablecollections.empty_iterable_exception import InvalidOperationError
from test_q_iterable_common import CallCounter, select_test, throws_test, value_test, where_test


def test_select() -> None:
    select_test((1, 2, 3), lambda x: x * 2, [2, 4, 6])

def test_single_returns_single_value() -> None: value_test([1], lambda x: x.single(), 1)
def test_single_throws_if_no_values() -> None: throws_test([], lambda x: x.single())
def test_single_throws_if_multiple_values() -> None: throws_test([1, 2], lambda x: x.single())
def test_single_returns_single_none_value() -> None: value_test([None], lambda x: x.single(), None)

def test_single_or_none_returns_single_value() -> None: value_test([1], lambda x: x.single_or_none(), 1)
def test_single_or_none_returns_none_if_no_values() -> None: value_test([], lambda x: x.single_or_none(), None)
def test_single_or_none_throws_if_multiple_values() -> None: throws_test([1, 2], lambda x: x.single_or_none(), InvalidOperationError)

def test_first_returns_first_value() -> None: value_test([1,2,3], lambda x: x.first(), 1)
def test_first_throws_if_no_values() -> None: throws_test([], lambda x: x.first())
def test_first_returns_single_none_value() -> None: value_test([None], lambda x: x.first(), None)

def test_first_or_none_returns_first_value() -> None: value_test([1,2,3], lambda x: x.first_or_none(), 1)
def test_first_or_none_return_none_if_no_values() -> None: value_test([], lambda x: x.first_or_none(), None)
def test_first_or_none_returns_single_none_value() -> None: value_test([None], lambda x: x.first_or_none(), None)

def test_where_first_element() -> None: where_test((1, 2, 3), lambda x: x == 1, [1])
def test_where_middle_element() -> None: where_test((1, 2, 3), lambda x: x == 2, [2])
def test_where_end_element() -> None: where_test((1, 2, 3), lambda x: x == 3, [3])

def test_element_at_returns_first_element() -> None: value_test([1, 2, 3], lambda x: x.element_at(0), 1)
def test_element_at_return_middle_element() -> None: value_test([1, 2, 3], lambda x: x.element_at(1), 2)
def test_element_at_returns_last_element() -> None: value_test([1, 2, 3], lambda x: x.element_at(2), 3)
def test_element_at_throws_if_index_is_out_of_range() -> None: throws_test((1, 2, 3), lambda x: x.element_at(3), IndexError)
def test_element_at_after_to_list_throws_if_index_is_out_of_range() -> None: throws_test((1, 2, 3), lambda x: x.element_at(3), IndexError)

def test_element_at_or_none_returns_first_element() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(0), 1)
def test_element_at_or_none_return_middle_element() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(1), 2)
def test_element_at_or_none_returns_last_element() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(2), 3)
def test_element_at_or_none_returns_none_if_index_is_out_of_range() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(3), None)
def test_element_at_or_none_after_to_list_returns_none_if_index_is_out_of_range() -> None: value_test([1, 2, 3], lambda x: x.element_at_or_none(3), None)

def test_where_excluding_first_element() -> None: where_test((1, 2, 3), lambda x: x != 1, [2, 3])
def test_where_excluding_middle_element() -> None: where_test((1, 2, 3), lambda x: x != 2, [1, 3])
def test_where_excluding_end_element() -> None: where_test((1, 2, 3), lambda x: x != 3, [1, 2])

def test_to_list() -> None: value_test([1, 2, 3], lambda x: x.to_list(), [1, 2, 3])
def test_to_sequence() -> None: value_test([1, 2, 3], lambda x: x.to_sequence().to_list(), [1, 2, 3])
def test_to_builtin_list() -> None: value_test([1, 2, 3], lambda x: x.to_built_in_list(), [1, 2, 3])
def test_to_set() -> None: value_test([1, 2, 3], lambda x: x.to_set(), {1, 2, 3})
def test_to_frozenset() -> None: value_test([1, 2, 3], lambda x: x.to_frozenset(), frozenset({1, 2, 3}))

def test_concat_appends_second_sequence_to_first() -> None: value_test([1, 2], lambda x: x.concat([3, 4]).to_list(), [1, 2, 3, 4])

def test_any_returns_true_if_there_are_elements() -> None: value_test([1], lambda x: x.any(), True)
def test_any_returns_false_if_there_are_no_elements() -> None: value_test([], lambda x: x.any(), False)

def test_indexer_returns_first_value() -> None: value_test([1, 2, 3], lambda x: x.to_list()[0], 1)
def test_indexer_returns_middle_value() -> None: value_test([1, 2, 3], lambda x: x.to_list()[1], 2)
def test_indexer_returns_last_value() -> None: value_test([1, 2, 3], lambda x: x.to_list()[2], 3)

def test_none_returns_false_if_there_are_elements() -> None: value_test([1], lambda x: x.none(), False)
def test_none_returns_true_if_there_are_no_elements() -> None: value_test([], lambda x: x.none(), True)

def test_distinct_removes_duplicates_while_retaining_order() -> None: value_test([1, 2, 2, 3, 3], lambda x: x.distinct().to_list(), [1, 2, 3])

def test_select_many_flattens_nested_sequences() -> None: value_test([[1, 2], [3, 4]], lambda x: x.select_many(lambda y: y).to_list(), [1, 2, 3, 4], skip_sets=True)

def test_reverse_returns_reversed_sequence() -> None: value_test([1, 2, 3], lambda x: x.reversed().to_list(), [3, 2, 1])

def test_not_none_returns_only_elements_that_are_not_none() -> None: value_test([1, None], lambda x: x.where_not_none().to_list(), [1])
def test_not_none_returns_empty_list_if_all_elements_are_none() -> None: value_test(QList[str | None]([None, None]), lambda x: x.where_not_none().to_list(), list[str]())

def test_assert_each_throws_if_any_element_does_not_match_predicate() -> None: throws_test([1, 2, 3], lambda x: x.assert_each(lambda y: y != 2), Exception)
def test_assert_each_does_not_throw_if_all_elements_match_predicate() -> None: value_test([1, 2, 3], lambda x: x.assert_each(lambda y: y != 0).to_list(), [1, 2, 3])

def test_order_by_sorts_in_ascending_order() -> None: value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).to_list(), [1, 2, 3])
def test_order_by_descending_sorts_in_descending_order() -> None: value_test([3, 2, 1], lambda x: x.order_by_descending(lambda y: y).to_list(), [3, 2, 1])
def test_then_by_sorts_in_ascending_order() -> None:
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by(lambda y: y).to_list(), [1, 2, 3])
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by(lambda y: 1 if y == 1 else 0).to_list(), [2, 3, 1])
def test_then_by_descending_sorts_in_descending_order() -> None:
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by_descending(lambda y: y).to_list(), [3, 2, 1])
    value_test([3, 2, 1], lambda x: x.order_by(lambda y: y).then_by_descending(lambda y: 1 if y == 2 else 0).to_list(), [2, 1, 3])

def test_length_returns_length_of_sequence() -> None:
    value_test([0], lambda x: x.qcount(), 1)
    value_test([0, 3], lambda x: x.qcount(), 2)
    value_test([0, 3, 5], lambda x: x.qcount(), 3)

def test_for_each_executes_action_for_each_element() -> None:
    value_test(lambda: [CallCounter(), CallCounter(), CallCounter()],
               lambda x: x.for_each(lambda y: y.increment()).select(lambda y: y.call_count).to_list(),
               [1, 1, 1])

def test_for_single_throws_if_there_are_no_elements() -> None:
    throws_test([], lambda x: x.for_single(lambda _: 1), Exception)

def test_for_single_throws_if_there_are_multiple_elements() -> None:
    throws_test([1, 2], lambda x: x.for_single(lambda _: 1), Exception)

def test_for_single_executes_action_if_there_is_exactly_one_element() -> None:
    value_test(lambda: [CallCounter()],
               lambda x: x.for_single(lambda y: y.increment()).select(lambda z: z.call_count).to_list(),
               [1])

def test_for_single_or_none_does_nothing_if_there_are_no_elements() -> None:
    value_test(QList[str]([]), lambda x: x.for_single_or_none(lambda _: 1).to_list(), list[str]())

def test_for_single_or_none_throws_if_there_are_multiple_elements() -> None:
    throws_test([1, 2], lambda x: x.for_single_or_none(lambda _: 1), Exception)

def test_for_single_or_none_executes_action_if_there_is_exactly_one_element() -> None:
    value_test(lambda: [CallCounter()],
               lambda x: x.for_single_or_none(lambda y: y.increment()).select(lambda z: z.call_count).to_list(),
               [1])

def test_assert_on_collection_throws_if_predicate_returns_false() -> None:
    throws_test([1, 2], lambda x: x.assert_on_collection(lambda _: False), Exception)

def test_assert_on_collection_does_not_throw_if_predicate_returns_true() -> None:
    value_test([1, 2], lambda x: x.assert_on_collection(lambda _: True).to_list(), [1, 2])