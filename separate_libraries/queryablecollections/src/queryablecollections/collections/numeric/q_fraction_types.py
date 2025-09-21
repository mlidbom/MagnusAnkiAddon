from __future__ import annotations

import statistics
from abc import ABC
from fractions import Fraction
from typing import TYPE_CHECKING, override

from queryablecollections._private_implementation_details.q_lazy_iterable import QIterableImplementation
from queryablecollections.collections.q_frozen_set import QFrozenSet
from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_sequence import QImmutableSequence
from queryablecollections.collections.q_set import QSet
from queryablecollections.q_errors import EmptyIterableError
from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Func

class QFractionIterable(QIterable[Fraction], ABC):
    __slots__: tuple[str, ...] = ()

    def sum(self) -> Fraction: return sum(self, Fraction(0))

    def min(self) -> Fraction:
        try:
            return min(self)
        except ValueError:
            raise EmptyIterableError() from None

    def max(self) -> Fraction:
        try:
            return max(self)
        except ValueError:
            raise EmptyIterableError() from None

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

class QFractionIterableImplementation(QIterableImplementation[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[Fraction]]) -> None:
        super().__init__(factory)

class QFractionList(QList[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)

class QFractionSet(QSet[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)

class QFractionFrozenSet(QFrozenSet[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[Fraction] = ()) -> QFractionFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QFractionSequence(QImmutableSequence[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)
