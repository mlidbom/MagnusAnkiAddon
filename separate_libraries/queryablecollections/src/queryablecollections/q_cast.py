from __future__ import annotations

from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from queryablecollections.collections.numeric.q_decimal_types import QIterableDecimalImplementation
    from queryablecollections.collections.numeric.q_float_types import QIterableFloat
    from queryablecollections.collections.numeric.q_fraction_types import QIterableFraction
    from queryablecollections.collections.numeric.q_int_types import QIterableInt
    from queryablecollections.q_iterable import QIterable

# noinspection DuplicatedCode
def _checked_cast_int(item: object) -> int:
    if not isinstance(item, int): raise TypeError(f"Expected int, got {type(item).__name__}")
    return item

def _checked_cast_float(item: object) -> float:
    if not isinstance(item, float): raise TypeError(f"Expected float, got {type(item).__name__}")
    return item

# noinspection DuplicatedCode
def _checked_cast_fraction(item: object) -> Fraction:
    if not isinstance(item, Fraction): raise TypeError(f"Expected Fraction, got {type(item).__name__}")
    return item

def _checked_cast_decimal(item: object) -> Decimal:
    if not isinstance(item, Decimal): raise TypeError(f"Expected Decimal, got {type(item).__name__}")
    return item

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

    def to[TNew](self, type: type[TNew]) -> QIterable[TNew]:  # pyright: ignore [reportInvalidTypeVarUse]
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
