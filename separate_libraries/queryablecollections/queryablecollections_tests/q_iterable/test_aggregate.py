from __future__ import annotations

from queryablecollections.q_errors import EmptyIterableError
from test_common_helpers import QList, lists_value_test, throws_test


def test_summing_numbers_returns_sum_of_the_elements() -> None:
    lists_value_test([1, 2, 3, 4, 5],
                     lambda x: x.aggregate(lambda acc, item: acc + item),
                     15)

def test_concatenates_strings_returns_all_strings_combined() -> None:
    lists_value_test(["hello", " ", "world", "!"],
                     lambda x: x.aggregate(lambda acc, item: acc + item),
                     "hello world!")

def test_aggregate_single_element_returns_that_element() -> None:
    lists_value_test([42],
                     lambda x: x.aggregate(lambda acc, item: acc + item),
                     42)

def test_aggregate_throws_on_empty_sequence() -> None:
    throws_test(QList[int](),
                lambda x: x.aggregate(lambda acc, item: acc + item),
                EmptyIterableError)