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

class QIntIterable(QIterable[int], ABC):
    __slots__: tuple[str, ...] = ()

    def sum(self) -> int: return sum(self)

    def min(self) -> int:
        try:
            return min(self)
        except ValueError:
            raise EmptyIterableError() from None

    def max(self) -> int:
        try:
            return max(self)
        except ValueError:
            raise EmptyIterableError() from None

    def min_or_default(self) -> int: return min(self) if self.any() else 0
    def max_or_default(self) -> int: return max(self) if self.any() else 0
    def average(self) -> float: return statistics.mean(self._assert_not_empty())
    def average_or_default(self) -> float: return statistics.mean(self) if self.any() else 0

    @override
    def to_list(self) -> QIntList: return QIntList(self)

    @override
    def to_sequence(self) -> QIntSequence: return QIntSequence(self)

    @override
    def to_set(self) -> QIntSet: return QIntSet(self)

    @override
    def to_frozenset(self) -> QIntFrozenSet: return QIntFrozenSet(self)

class QIntIterableImplementation(QIterableImplementation[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[int]]) -> None:
        super().__init__(factory)

class QIntList(QList[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[int] = ()) -> None:
        super().__init__(iterable)

class QIntSet(QSet[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[int] = ()) -> None:
        super().__init__(iterable)

class QIntFrozenSet(QFrozenSet[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[int] = ()) -> QIntFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QIntSequence(QImmutableSequence[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[int] = ()) -> None:
        super().__init__(iterable)
