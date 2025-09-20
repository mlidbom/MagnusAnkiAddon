from __future__ import annotations

from decimal import Decimal

from queryablecollections.collections.numeric.q_decimal_types import QDecimalList
from queryablecollections.empty_iterable_exception import EmptyIterableError
from test_q_iterable_common import *


def test_cast_decimal_returns_an_q_iterable_decimal_with_the_same_elements() -> None:
    value_test([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")], lambda x: x.cast.decimal().to_list(), [Decimal("1.1"), Decimal("2.1"), Decimal("3.1")])

def test_cast_checked_decimal_returns_a_q_iterable_decimal_with_the_same_elements() -> None:
    value_test([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")], lambda x: x.cast.checked.decimal().to_list(), [Decimal("1.1"), Decimal("2.1"), Decimal("3.1")])

def test_cast_checked_decimal_raises_type_error_if_collection_contains_non_decimal() -> None:
    throws_test([Decimal("1.1"), "2.1", Decimal("3.1")], lambda x: x.cast.checked.decimal().to_list(), TypeError)

def test_sum_returns_sum_of_the_values() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).sum() == Decimal("6.3")
def test_sum_returns_zero_on_on_empty_collection() -> None: assert QDecimalList().sum() == Decimal(0)

def test_min_returns_min_of_the_values() -> None: assert QDecimalList([Decimal("6.1"), Decimal("2.1"), Decimal("5.1"), Decimal("3.1")]).min() == Decimal("2.1")
def test_min_raises_invalid_operation_on_on_empty_collection() -> None:
    with pytest.raises(EmptyIterableError): QDecimalList().min()

def test_min_or_default_returns_min_of_the_values() -> None: assert QDecimalList([Decimal("6.1"), Decimal("2.1"), Decimal("5.1"), Decimal("3.1")]).min_or_default() == Decimal("2.1")
def test_min_or_default_returns_0_on_on_empty_collection() -> None: assert QDecimalList().min_or_default() == Decimal(0)

def test_max_returns_max_of_the_values() -> None: assert QDecimalList([Decimal("1.1"), Decimal("5.1"), Decimal("3.1")]).max() == Decimal("5.1")
def test_max_raises_invalid_operation_on_on_empty_collection() -> None:
    with pytest.raises(EmptyIterableError): QDecimalList().max()

def test_max_or_default_returns_max_of_the_values() -> None: assert QDecimalList([Decimal("1.1"), Decimal("5.1"), Decimal("3.1")]).max_or_default() == Decimal("5.1")
def test_max_or_default_returns_0_on_on_empty_collection() -> None: assert QDecimalList().max_or_default() == Decimal(0)

def test_average_returns_average_of_the_values() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).average() == Decimal("2.1")
def test_average_throws_on_on_empty_collection() -> None:
    with pytest.raises(EmptyIterableError): QDecimalList().average()

def test_average_or_default_returns_average_of_the_values() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).average_or_default() == Decimal("2.1")
def test_average_or_default_returns_0_on_on_empty_collection() -> None: assert QDecimalList().average_or_default() == Decimal(0)

def test_to_list_returns_a_list_with_the_same_elements() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).to_list() == [Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]
def test_to_set_returns_a_set_with_the_same_elements() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).to_set() == {Decimal("1.1"), Decimal("2.1"), Decimal("3.1")}
def test_to_frozenset_returns_a_frozenset_with_the_same_elements() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).to_frozenset() == frozenset({Decimal("1.1"), Decimal("2.1"), Decimal("3.1")})
def test_to_sequence_returns_a_sequence_with_the_same_elements() -> None: assert QDecimalList([Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]).to_sequence().to_list() == [Decimal("1.1"), Decimal("2.1"), Decimal("3.1")]
