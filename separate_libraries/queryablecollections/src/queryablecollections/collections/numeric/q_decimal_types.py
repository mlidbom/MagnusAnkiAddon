from __future__ import annotations

import statistics
from abc import ABC
from decimal import Decimal
from typing import TYPE_CHECKING, cast, override

from queryablecollections._private_implementation_details.q_lazy_iterable import QLazyIterableImplementation
from queryablecollections._private_implementation_details.sort_instruction import SortInstruction
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
    def _lazy(self, factory: Func[Iterable[Decimal]]) -> QDecimalIterable: return QDecimalIterableImplementation(factory)
    @override
    def _order_by(self, key_selector: Selector[Decimal, SupportsRichComparison], descending: bool) -> QOrderedIterable[Decimal]:
        return QDecimalOrderedIterable(lambda: self, [SortInstruction(key_selector, descending)])
    def _selfcast(self, iterable: QIterable[Decimal]) -> QDecimalIterable: return cast(QDecimalIterable, iterable)
    def _selfcast_ordered(self, iterable: QOrderedIterable[Decimal]) -> QDecimalOrderedIterable: return cast(QDecimalOrderedIterable, iterable)

    # region override methods so that typecheckers know that we actually return QDecimalIterables now, not QIterable[Decimal]
    # call the base method to eliminate code duplication. The base class will call lazy from just above, so it is already the correct type
    @override
    def where(self, predicate: Predicate[Decimal]) -> QDecimalIterable: return self._selfcast(super().where(predicate))
    @override
    def where_not_none(self) -> QDecimalIterable: return self._selfcast(super().where_not_none())
    @override
    def distinct(self) -> QDecimalIterable: return self._selfcast(super().distinct())
    @override
    def distinct_by[TKey](self, key_selector: Selector[Decimal, TKey]) -> QDecimalIterable: return self._selfcast(super().distinct_by(key_selector))
    @override
    def take(self, count: int) -> QDecimalIterable: return self._selfcast(super().take(count))
    @override
    def take_while(self, predicate: Predicate[Decimal]) -> QDecimalIterable: return self._selfcast(super().take_while(predicate))
    @override
    def take_last(self, count: int) -> QDecimalIterable: return self._selfcast(super().take_last(count))
    @override
    def skip(self, count: int) -> QDecimalIterable: return self._selfcast(super().skip(count))
    @override
    def skip_last(self, count: int) -> QDecimalIterable: return self._selfcast(super().skip_last(count))
    @override
    def reversed(self) -> QDecimalIterable: return self._selfcast(super().reversed())

    @override
    def concat(self, *others: Iterable[Decimal]) -> QDecimalIterable: return self._selfcast(super().concat(*others))

    @override
    def order_by(self, key_selector: Selector[Decimal, SupportsRichComparison]) -> QDecimalOrderedIterable: return self._selfcast_ordered(super().order_by(key_selector))
    @override
    def order_by_descending(self, key_selector: Selector[Decimal, SupportsRichComparison]) -> QDecimalOrderedIterable: return self._selfcast_ordered(super().order_by_descending(key_selector))
    # endregion

    @override
    def to_list(self) -> QDecimalList: return QDecimalList(self)

    @override
    def to_sequence(self) -> QDecimalSequence: return QDecimalSequence(self)

    @override
    def to_set(self) -> QDecimalSet: return QDecimalSet(self)

    @override
    def to_frozenset(self) -> QDecimalFrozenSet: return QDecimalFrozenSet(self)

class QDecimalIterableImplementation(QLazyIterableImplementation[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[Decimal]]) -> None:
        super().__init__(factory)

class QDecimalOrderedIterable(QOrderedIterable[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[Decimal]], sorting_instructions: list[SortInstruction[Decimal]]) -> None:
        super().__init__(factory, sorting_instructions)

class QDecimalList(QList[Decimal], QDecimalIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Decimal] = ()) -> None:
        super().__init__(iterable)

    @override
    def reversed(self) -> QDecimalIterable: return QDecimalIterable.reversed(self)

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

    @override
    def reversed(self) -> QDecimalIterable: return QDecimalIterable.reversed(self)
