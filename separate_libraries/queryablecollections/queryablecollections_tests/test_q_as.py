from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from queryablecollections.collections.numeric.q_decimal_types import QIterableDecimal
from queryablecollections.collections.numeric.q_float_types import QIterableFloat
from queryablecollections.collections.numeric.q_fraction_types import QIterableFraction
from queryablecollections.collections.numeric.q_int_types import QIterableInt
from queryablecollections.collections.q_list import QList


def test_as_int_returns_an_q_iterable_int_with_all_the_values_in_order() -> None:
    # test = QList(("1", "2", "3")).as_int() #typing error
    test = QList(("1", "2", "3")).select(int).auto_type()

    assert test.to_list() == [1, 2, 3]
    assert isinstance(test, QIterableInt)

def test_as_float_returns_an_q_iterable_float_with_all_the_values_in_order() -> None:
    # test = QList(("1.1", "2.1", "3.1")).as_float() #typing error
    # test = QList(("1", "2", "3")).select(int).as_float() # typing error
    test = QList(("1.1", "2.1", "3.1")).select(float).auto_type()

    assert test.to_list() == [1.1, 2.1, 3.1]
    assert isinstance(test, QIterableFloat)

def test_as_fraction_returns_an_q_iterable_fraction_with_all_the_values_in_order() -> None:
    # test = QList(("1.1", "2.1", "3.1")).as_fraction() #typing error
    # test = QList(("1", "2", "3")).select(int).as_fraction() # typing error
    test = QList((Fraction(1, 2), Fraction(2, 3))).auto_type()

    assert test.to_list() == [Fraction(1, 2), Fraction(2, 3)]
    assert isinstance(test, QIterableFraction)

def test_as_decimal_returns_an_q_iterable_decimal_with_all_the_values_in_order() -> None:
    # test = QList(("1.1", "2.1", "3.1")).as_decimal() #typing error
    # test = QList(("1", "2", "3")).select(int).as_decimal() # typing error
    test = QList((Decimal("1.2"), Decimal("2.1"))).auto_type()

    assert test.to_list() == [Decimal("1.2"), Decimal("2.1")]
    assert isinstance(test, QIterableDecimal)
