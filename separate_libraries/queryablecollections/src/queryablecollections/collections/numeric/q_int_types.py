from __future__ import annotations

import statistics
from abc import ABC
from typing import TYPE_CHECKING, cast, override

from queryablecollections._private_implementation_details.operations.ordering import SortInstruction
from queryablecollections._private_implementation_details.q_lazy_iterable import QLazyIterableImplementation
from queryablecollections.collections.q_frozen_set import QFrozenSet
from queryablecollections.collections.q_immutable_sequence import QImmutableSequence
from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_set import QSet
from queryablecollections.q_errors import EmptyIterableError
from queryablecollections.q_iterable import QIterable
from queryablecollections.q_ordered_iterable import QOrderedIterable

if TYPE_CHECKING:
    from collections.abc import Iterable

    from _typeshed import SupportsRichComparison

    from queryablecollections._private_implementation_details.type_aliases import Func, Predicate, Selector

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
    def average_or_default(self) -> float: return statistics.mean(self) if self.any() else 0.0

    @override
    def _lazy(self, factory: Func[Iterable[int]]) -> QIntIterable: return QIntIterableImplementation(factory)
    @override
    def _order_by(self, key_selector: Selector[int, SupportsRichComparison], descending: bool) -> QOrderedIterable[int]:
        return QIntOrderedIterable(lambda: self, [SortInstruction(key_selector, descending)])
    def _selfcast(self, iterable: QIterable[int]) -> QIntIterable: return cast(QIntIterable, iterable)
    def _selfcast_ordered(self, iterable: QOrderedIterable[int]) -> QIntOrderedIterable: return cast(QIntOrderedIterable, iterable)

    # region override methods so that typecheckers know that we actually return QIntIterables now, not QIterable[int]
    # call the base method to eliminate code duplication. The base class will call lazy from just above, so it is already the correct type
    @override
    def where(self, predicate: Predicate[int]) -> QIntIterable: return self._selfcast(super().where(predicate))
    @override
    def where_not_none(self) -> QIntIterable: return self._selfcast(super().where_not_none())
    @override
    def distinct(self) -> QIntIterable: return self._selfcast(super().distinct())
    @override
    def distinct_by[TKey](self, key_selector: Selector[int, TKey]) -> QIntIterable: return self._selfcast(super().distinct_by(key_selector))
    @override
    def take(self, count: int) -> QIntIterable: return self._selfcast(super().take(count))
    @override
    def take_while(self, predicate: Predicate[int]) -> QIntIterable: return self._selfcast(super().take_while(predicate))
    @override
    def take_last(self, count: int) -> QIntIterable: return self._selfcast(super().take_last(count))
    @override
    def skip(self, count: int) -> QIntIterable: return self._selfcast(super().skip(count))
    @override
    def skip_last(self, count: int) -> QIntIterable: return self._selfcast(super().skip_last(count))
    @override
    def reversed(self) -> QIntIterable: return self._selfcast(super().reversed())

    @override
    def concat(self, *others: Iterable[int]) -> QIntIterable: return self._selfcast(super().concat(*others))

    @override
    def order_by(self, key_selector: Selector[int, SupportsRichComparison]) -> QIntOrderedIterable: return self._selfcast_ordered(super().order_by(key_selector))
    @override
    def order_by_descending(self, key_selector: Selector[int, SupportsRichComparison]) -> QIntOrderedIterable: return self._selfcast_ordered(super().order_by_descending(key_selector))
    # endregion

    @override
    def to_list(self) -> QIntList: return QIntList(self)

    @override
    def to_sequence(self) -> QIntSequence: return QIntSequence(self)

    @override
    def to_set(self) -> QIntSet: return QIntSet(self)

    @override
    def to_frozenset(self) -> QIntFrozenSet: return QIntFrozenSet(self)

class QIntIterableImplementation(QLazyIterableImplementation[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[int]]) -> None:
        super().__init__(factory)

class QIntOrderedIterable(QOrderedIterable[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[int]], sorting_instructions: list[SortInstruction[int]]) -> None:
        super().__init__(factory, sorting_instructions)

class QIntList(QList[int], QIntIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[int] = ()) -> None:
        super().__init__(iterable)

    @override
    def reversed(self) -> QIntIterable: return QIntIterable.reversed(self)

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

    @override
    def reversed(self) -> QIntIterable: return QIntIterable.reversed(self)
