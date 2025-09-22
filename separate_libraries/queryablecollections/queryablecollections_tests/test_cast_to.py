from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from common_helpers import lists_value_test


def test_to_int_returns_q_iterable_with_same_elements() -> None:
    lists_value_test([1, 2, 3],
                     lambda x: x.cast.to(int).to_list(),
                     [1, 2, 3])

def test_to_str_returns_q_iterable_with_same_elements() -> None:
    lists_value_test(["a", "b", "c"],
                     lambda x: x.cast.to(str).to_list(),
                     ["a", "b", "c"])

def test_to_fraction_q_iterable_with_same_elements() -> None:
    lists_value_test([Fraction(1, 2), Fraction(3, 4)],
                     lambda x: x.cast.to(Fraction).to_list(),
                     [Fraction(1, 2), Fraction(3, 4)])

def test_to_decimal_returns_q_iterable_with_same_elements() -> None:
    lists_value_test([Decimal("1.5"), Decimal("2.7")],
                     lambda x: x.cast.to(Decimal).to_list(),
                     [Decimal("1.5"), Decimal("2.7")])
