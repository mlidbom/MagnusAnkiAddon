from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from queryablecollections.collections.numeric.q_decimal_types import QDecimalIterable
from queryablecollections.collections.numeric.q_float_types import QFloatIterable
from queryablecollections.collections.numeric.q_fraction_types import QFractionIterable
from queryablecollections.collections.numeric.q_int_types import QIntIterable
from queryablecollections.collections.q_list import QList


def test_iterable_of_int_returns_an_int_iterable_with_all_the_values_in_order() -> None:
    test = QList(("1", "2", "3")).select(int).as_ints()

    assert test.to_list() == [1, 2, 3]
    assert isinstance(test, QIntIterable)

def test_iterable_of_float_returns_a_float_iterable_with_all_the_values_in_order() -> None:
    test = QList(("1.1", "2.1", "3.1")).select(float).as_floats()

    assert test.to_list() == [1.1, 2.1, 3.1]
    assert isinstance(test, QFloatIterable)

def test_iterable_of_fraction_returns_a_fraction_iterable_with_all_the_values_in_order() -> None:
    test = QList((Fraction(1, 2), Fraction(2, 3))).as_fractions()

    assert test.to_list() == [Fraction(1, 2), Fraction(2, 3)]
    assert isinstance(test, QFractionIterable)

def test_iterable_of_decimal_returns_a_decimal_iterable_with_all_the_values_in_order() -> None:
    test = QList((Decimal("1.2"), Decimal("2.1"))).as_decimals()

    assert test.to_list() == [Decimal("1.2"), Decimal("2.1")]
    assert isinstance(test, QDecimalIterable)