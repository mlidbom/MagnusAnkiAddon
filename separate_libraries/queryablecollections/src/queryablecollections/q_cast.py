from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING, cast

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from queryablecollections.collections.numeric.q_decimal_types import QIterableDecimalImplementation
    from queryablecollections.collections.numeric.q_float_types import QIterableFloat
    from queryablecollections.collections.numeric.q_fraction_types import QIterableFraction
    from queryablecollections.collections.numeric.q_int_types import QIterableInt

class CheckedCast[TValue]:
    __slots__: tuple[str, ...] = ("_type",)
    def __init__(self, type: type[TValue]) -> None:
        self._type: type[TValue] = type

    def __call__(self, value: object) -> TValue:
        if not isinstance(value, self._type): raise TypeError(f"Expected {self._type.__name__}, got {type(value).__name__}")
        return value

_checked_cast_int = CheckedCast(int)
_checked_cast_float = CheckedCast(float)
_checked_cast_fraction = CheckedCast(Fraction)
_checked_cast_decimal = CheckedCast(Decimal)

class QCast[TItem]:
    __slots__: tuple[str, ...] = ("_iterable",)
    def __init__(self, iterable: QIterable[TItem]) -> None:
        self._iterable: QIterable[TItem] = iterable

    @property
    def checked(self) -> QCheckedCast[TItem]:
        return QCheckedCast(self._iterable)

    def int(self) -> QIterableInt:
        from queryablecollections.collections.numeric.q_int_types import QIterableIntImplementation
        return QIterableIntImplementation(cast(Iterable[int], self._iterable))

    def float(self) -> QIterableFloat:
        from queryablecollections.collections.numeric.q_float_types import QIterableFloatImplementation
        return QIterableFloatImplementation(cast(Iterable[float], self._iterable))

    def fraction(self) -> QIterableFraction:
        from queryablecollections.collections.numeric.q_fraction_types import QIterableFractionImplementation
        return QIterableFractionImplementation(cast(Iterable[Fraction], self._iterable))

    def decimal(self) -> QIterableDecimalImplementation:
        from queryablecollections.collections.numeric.q_decimal_types import QIterableDecimalImplementation
        return QIterableDecimalImplementation(cast(Iterable[Decimal], self._iterable))

    def to[TNew](self, _type: type[TNew]) -> QIterable[TNew]:  # pyright: ignore
        return cast(QIterable[TNew], self._iterable)

class QCheckedCast[TItem]:
    __slots__: tuple[str, ...] = ("_iterable",)
    def __init__(self, iterable: QIterable[TItem]) -> None:
        self._iterable: QIterable[TItem] = iterable

    def int(self) -> QIterableInt:
        from queryablecollections.collections.numeric.q_int_types import QIterableIntImplementation
        return QIterableIntImplementation(self._iterable.select(_checked_cast_int))

    def float(self) -> QIterableFloat:
        from queryablecollections.collections.numeric.q_float_types import QIterableFloatImplementation
        return QIterableFloatImplementation(self._iterable.select(_checked_cast_float))

    def fraction(self) -> QIterableFraction:
        from queryablecollections.collections.numeric.q_fraction_types import QIterableFractionImplementation
        return QIterableFractionImplementation(self._iterable.select(_checked_cast_fraction))

    def decimal(self) -> QIterableDecimalImplementation:
        from queryablecollections.collections.numeric.q_decimal_types import QIterableDecimalImplementation
        return QIterableDecimalImplementation(self._iterable.select(_checked_cast_decimal))

    def to[TNew](self, _type: type[TNew]) -> QIterable[TNew]:  # pyright: ignore
        return self._iterable.select(CheckedCast(_type))
