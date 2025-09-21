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

class QFloatIterable(QIterable[float], ABC):
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

    def min_or_default(self) -> float: return min(self) if self.any() else 0.0
    def max_or_default(self) -> float: return max(self) if self.any() else 0.0
    def average(self) -> float: return statistics.mean(self._assert_not_empty())
    def average_or_default(self) -> float: return statistics.mean(self) if self.any() else 0.0

    @override
    def _lazy(self, factory: Func[Iterable[float]]) -> QFloatIterable: return QFloatIterableImplementation(factory)
    @override
    def _order_by(self, key_selector: Selector[float, SupportsRichComparison], descending: bool) -> QOrderedIterable[float]:
        return QFloatOrderedIterable(lambda: self, [SortInstruction(key_selector, descending)])
    def _selfcast(self, iterable: QIterable[float]) -> QFloatIterable: return cast(QFloatIterable, iterable)
    def _selfcast_ordered(self, iterable: QOrderedIterable[float]) -> QFloatOrderedIterable: return cast(QFloatOrderedIterable, iterable)

    # region override methods so that typecheckers know that we actually return QFloatIterables now, not QIterable[float]
    # call the base method to eliminate code duplication. The base class will call lazy from just above, so it is already the correct type
    @override
    def where(self, predicate: Predicate[float]) -> QFloatIterable: return self._selfcast(super().where(predicate))
    @override
    def where_not_none(self) -> QFloatIterable: return self._selfcast(super().where_not_none())
    @override
    def distinct(self) -> QFloatIterable: return self._selfcast(super().distinct())
    @override
    def take(self, count: int) -> QFloatIterable: return self._selfcast(super().take(count))
    @override
    def take_while(self, predicate: Predicate[float]) -> QFloatIterable: return self._selfcast(super().take_while(predicate))
    @override
    def take_last(self, count: int) -> QFloatIterable: return self._selfcast(super().take_last(count))
    @override
    def skip(self, count: int) -> QFloatIterable: return self._selfcast(super().skip(count))
    @override
    def skip_last(self, count: int) -> QFloatIterable: return self._selfcast(super().skip_last(count))
    @override
    def reversed(self) -> QFloatIterable: return self._selfcast(super().reversed())

    @override
    def concat(self, *others: Iterable[float]) -> QFloatIterable: return self._selfcast(super().concat(*others))

    @override
    def ordered(self) -> QFloatIterable: return self._selfcast(super().ordered())
    @override
    def order_by(self, key_selector: Selector[float, SupportsRichComparison]) -> QFloatOrderedIterable: return self._selfcast_ordered(super().order_by(key_selector))
    @override
    def order_by_descending(self, key_selector: Selector[float, SupportsRichComparison]) -> QFloatOrderedIterable: return self._selfcast_ordered(super().order_by_descending(key_selector))
    # endregion

    @override
    def to_list(self) -> QFloatList: return QFloatList(self)

    @override
    def to_sequence(self) -> QFloatSequence: return QFloatSequence(self)

    @override
    def to_set(self) -> QFloatSet: return QFloatSet(self)

    @override
    def to_frozenset(self) -> QFloatFrozenSet: return QFloatFrozenSet(self)

class QFloatIterableImplementation(QLazyIterableImplementation[float], QFloatIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[float]]) -> None:
        super().__init__(factory)

class QFloatOrderedIterable(QOrderedIterable[float], QFloatIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[float]], sorting_instructions: list[SortInstruction[float]]) -> None:
        super().__init__(factory, sorting_instructions)

class QFloatList(QList[float], QFloatIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[float] = ()) -> None:
        super().__init__(iterable)

    @override
    def reversed(self) -> QFloatIterable: return QFloatIterable.reversed(self)

class QFloatSet(QSet[float], QFloatIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[float] = ()) -> None:
        super().__init__(iterable)

class QFloatFrozenSet(QFrozenSet[float], QFloatIterable):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[float] = ()) -> QFloatFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QFloatSequence(QImmutableSequence[float], QFloatIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[float] = ()) -> None:
        super().__init__(iterable)

    @override
    def reversed(self) -> QFloatIterable: return QFloatIterable.reversed(self)
