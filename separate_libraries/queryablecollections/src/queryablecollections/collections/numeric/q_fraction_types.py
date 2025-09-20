from __future__ import annotations

import statistics
from abc import ABC
from fractions import Fraction
from typing import TYPE_CHECKING, override

from queryablecollections.collections.q_frozen_set import QFrozenSet
from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_sequence import QImmutableSequence
from queryablecollections.collections.q_set import QSet
from queryablecollections.q_iterable import QIterable, QiterableImplementation

if TYPE_CHECKING:
    from collections.abc import Iterable

class QIterableFraction(QIterable[Fraction], ABC):
    __slots__: tuple[str, ...] = ()

    def sum(self) -> Fraction: return sum(self, Fraction(0))
    def min(self) -> Fraction: return min(self._assert_not_empty())
    def max(self) -> Fraction: return max(self._assert_not_empty())
    def min_or_default(self) -> Fraction: return min(self) if self.any() else Fraction(0)
    def max_or_default(self) -> Fraction: return max(self) if self.any() else Fraction(0)
    def average(self) -> Fraction: return statistics.mean(self._assert_not_empty())
    def average_or_default(self) -> Fraction: return statistics.mean(self) if self.any() else Fraction(0)

    @override
    def to_list(self) -> QFractionList: return QFractionList(self)

    @override
    def to_sequence(self) -> QFractionSequence: return QFractionSequence(self)

    @override
    def to_set(self) -> QFractionSet: return QFractionSet(self)

    @override
    def to_frozenset(self) -> QFractionFrozenSet: return QFractionFrozenSet(self)

class QIterableFractionImplementation(QiterableImplementation[Fraction], QIterableFraction):
    __slots__: tuple[str, ...] = ()
    def __init__(self, value: Iterable[Fraction]) -> None:
        super().__init__(value)

class QFractionList(QList[Fraction], QIterableFraction):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)

class QFractionSet(QSet[Fraction], QIterableFraction):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)

class QFractionFrozenSet(QFrozenSet[Fraction], QIterableFraction):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[Fraction] = ()) -> QFractionFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QFractionSequence(QImmutableSequence[Fraction], QIterableFraction):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)
