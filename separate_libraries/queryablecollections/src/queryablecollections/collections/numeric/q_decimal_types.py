from __future__ import annotations

import statistics
from abc import ABC
from decimal import Decimal
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

class QDecimalIterable(QIterable[Decimal], ABC):
    __slots__: tuple[str, ...] = ()

    def sum(self) -> Decimal: return sum(self, Decimal(0))

    def min(self) -> Decimal:
        try:
            return min(self)
        except ValueError:
            raise EmptyIterableError() from None

    def max(self) -> Decimal:
        try:
            return max(self)
        except ValueError:
            raise EmptyIterableError() from None

    def min_or_default(self) -> Decimal: return min(self) if self.any() else Decimal(0)
    def max_or_default(self) -> Decimal: return max(self) if self.any() else Decimal(0)
    def average(self) -> Decimal: return statistics.mean(self._assert_not_empty())
    def average_or_default(self) -> Decimal: return statistics.mean(self) if self.any() else Decimal(0)

    @override
    def to_list(self) -> QDecimalList: return QDecimalList(self)

    @override
    def to_sequence(self) -> QDecimalSequence: return QDecimalSequence(self)

    @override
    def to_set(self) -> QDecimalSet: return QDecimalSet(self)

    @override
    def to_frozenset(self) -> QDecimalFrozenSet: return QDecimalFrozenSet(self)

class QDecimalIterableImplementation(QIterableImplementation[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[Decimal]]) -> None:
        super().__init__(factory)

class QDecimalList(QList[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Decimal] = ()) -> None:
        super().__init__(iterable)

class QDecimalSet(QSet[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Decimal] = ()) -> None:
        super().__init__(iterable)

class QDecimalFrozenSet(QFrozenSet[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[Decimal] = ()) -> QDecimalFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QDecimalSequence(QImmutableSequence[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Decimal] = ()) -> None:
        super().__init__(iterable)
