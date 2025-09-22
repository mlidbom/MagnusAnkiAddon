from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from test_iterable_common import lists_value_test, throws_test


class TestUncheckedCast:
    def test_to_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test([1, 2, 3],
                         lambda x: x.cast.to(int).to_list(),
                         [1, 2, 3])

    def test_to_with_string_type_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test(["a", "b", "c"],
                         lambda x: x.cast.to(str).to_list(),
                         ["a", "b", "c"])

    def test_with_fraction_type_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test([Fraction(1, 2), Fraction(3, 4)],
                         lambda x: x.cast.to(Fraction).to_list(),
                         [Fraction(1, 2), Fraction(3, 4)])

    def test_cast_to_with_decimal_type_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test([Decimal("1.5"), Decimal("2.7")],
                         lambda x: x.cast.to(Decimal).to_list(),
                         [Decimal("1.5"), Decimal("2.7")])

class TestCheckedCast:
    def test_cast_checked_to_returns_q_iterable_with_same_elements_when_types_match(self) -> None:
        lists_value_test([1, 2, 3],
                         lambda x: x.cast.checked.to(int).to_list(),
                         [1, 2, 3])

    def test_cast_checked_to_with_string_type_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test(["hello", "world"],
                         lambda x: x.cast.checked.to(str).to_list(),
                         ["hello", "world"])

    def test_with_fraction_type_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test([Fraction(1, 3), Fraction(2, 5)],
                         lambda x: x.cast.checked.to(Fraction).to_list(),
                         [Fraction(1, 3), Fraction(2, 5)])

    def test_cast_checked_to_with_decimal_type_returns_q_iterable_with_same_elements(self) -> None:
        lists_value_test([Decimal("1.23"), Decimal("4.56")],
                         lambda x: x.cast.checked.to(Decimal).to_list(),
                         [Decimal("1.23"), Decimal("4.56")])

    def test_raises_type_error_when_types_dont_match(self) -> None:
        throws_test([1, "2", 3],
                    lambda x: x.cast.checked.to(int).to_list(),
                    TypeError)

    def test_raises_type_error_for_mixed_string_int(self) -> None:
        throws_test(["hello", 42],
                    lambda x: x.cast.checked.to(str).to_list(),
                    TypeError)

    def test_raises_type_error_for_mixed_fraction_float(self) -> None:
        throws_test([Fraction(1, 3), 0.5],
                    lambda x: x.cast.checked.to(Fraction).to_list(),
                    TypeError)

    def test_raises_type_error_for_mixed_decimal_float(self) -> None:
        throws_test([Decimal("1.23"), 4.56],
                    lambda x: x.cast.checked.to(Decimal).to_list(),
                    TypeError)
