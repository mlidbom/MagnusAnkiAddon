from __future__ import annotations

import statistics
from abc import ABC
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

class QIterableFloat(QIterable[float], ABC):
    __slots__: tuple[str, ...] = ()

    def sum(self) -> float: return sum(self)

    def min(self) -> float:
        try:
            return min(self)
        except ValueError:
            raise EmptyIterableError() from None

    def max(self) -> float:
        try:
            return max(self)
        except ValueError:
            raise EmptyIterableError() from None

    def min_or_default(self) -> float: return min(self) if self.any() else 0
    def max_or_default(self) -> float: return max(self) if self.any() else 0
    def average(self) -> float: return statistics.mean(self._assert_not_empty())
    def average_or_default(self) -> float: return statistics.mean(self) if self.any() else 0

    @override
    def to_list(self) -> QFloatList: return QFloatList(self)

    @override
    def to_sequence(self) -> QFloatSequence: return QFloatSequence(self)

    @override
    def to_set(self) -> QFloatSet: return QFloatSet(self)

    @override
    def to_frozenset(self) -> QFloatFrozenSet: return QFloatFrozenSet(self)

class QIterableFloatImplementation(QIterableImplementation[float], QIterableFloat):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[float]]) -> None:
        super().__init__(factory)

class QFloatList(QList[float], QIterableFloat):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[float] = ()) -> None:
        super().__init__(iterable)

class QFloatSet(QSet[float], QIterableFloat):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[float] = ()) -> None:
        super().__init__(iterable)

class QFloatFrozenSet(QFrozenSet[float], QIterableFloat):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[float] = ()) -> QFloatFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QFloatSequence(QImmutableSequence[float], QIterableFloat):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[float] = ()) -> None:
        super().__init__(iterable)
