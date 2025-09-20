from __future__ import annotations

from queryablecollections.collections.numeric.q_int_types import QIntList
from queryablecollections.empty_iterable_exception import EmptyIterableError
from test_q_iterable_common import *


def test_cast_int_returns_an_q_iterable_int_with_the_same_elements() -> None:
    value_test([1, 2, 3], lambda x: x.cast.int().to_list(), [1, 2, 3])

def test_cast_checked_int_returns_a_q_iterable_int_with_the_same_elements() -> None:
    value_test([1, 2, 3], lambda x: x.cast.checked.int().to_list(), [1, 2, 3])

def test_cast_checked_int_raises_type_error_if_collection_contains_non_int() -> None:
    throws_test([1, "2", 3], lambda x: x.cast.checked.int().to_list(), TypeError)

def test_sum_returns_sum_of_the_values() -> None: assert QIntList([1, 2, 3]).sum() == 6
def test_sum_returns_zero_on_on_empty_collection() -> None: assert QIntList().sum() == 0

def test_min_returns_min_of_the_values() -> None: assert QIntList([6, 2, 5, 3]).min() == 2
def test_min_raises_invalid_operation_on_on_empty_collection() -> None:
    with pytest.raises(EmptyIterableError): QIntList().min()

def test_min_or_default_returns_min_of_the_values() -> None: assert QIntList([6, 2, 5, 3]).min_or_default() == 2
def test_min_or_default_returns_0_on_on_empty_collection() -> None: assert QIntList().min_or_default() == 0

def test_max_returns_max_of_the_values() -> None: assert QIntList([1, 5, 3]).max() == 5
def test_max_raises_invalid_operation_on_on_empty_collection() -> None:
    with pytest.raises(EmptyIterableError): QIntList().max()

def test_max_or_default_returns_max_of_the_values() -> None: assert QIntList([1, 5, 3]).max_or_default() == 5
def test_max_or_default_returns_0_on_on_empty_collection() -> None: assert QIntList().max_or_default() == 0

def test_average_returns_average_of_the_values() -> None: assert QIntList([1, 2, 3]).average() == 2
def test_average_throws_on_on_empty_collection() -> None:
    with pytest.raises(EmptyIterableError): QIntList().average()

def test_average_or_default_returns_average_of_the_values() -> None: assert QIntList([1, 2, 3]).average_or_default() == 2
def test_average_or_default_returns_0_on_on_empty_collection() -> None: assert QIntList().average_or_default() == 0

def test_to_list_returns_a_list_with_the_same_elements() -> None: assert QIntList([1, 2, 3]).to_list() == [1, 2, 3]
def test_to_set_returns_a_set_with_the_same_elements() -> None: assert QIntList([1, 2, 3]).to_set() == {1, 2, 3}
def test_to_frozenset_returns_a_frozenset_with_the_same_elements() -> None: assert QIntList([1, 2, 3]).to_frozenset() == frozenset({1, 2, 3})
def test_to_sequence_returns_a_sequence_with_the_same_elements() -> None: assert QIntList([1, 2, 3]).to_sequence().to_list() == [1, 2, 3]
