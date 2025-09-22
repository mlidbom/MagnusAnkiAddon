from __future__ import annotations

import statistics
from abc import ABC
from fractions import Fraction
from typing import TYPE_CHECKING, cast, override

from queryablecollections._private_implementation_details.sort_instruction import SortInstruction
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
    def _lazy(self, factory: Func[Iterable[Fraction]]) -> QFractionIterable: return QFractionIterableImplementation(factory)
    @override
    def _order_by(self, key_selector: Selector[Fraction, SupportsRichComparison], descending: bool) -> QOrderedIterable[Fraction]:
        return QFractionOrderedIterable(lambda: self, [SortInstruction(key_selector, descending)])
    def _selfcast(self, iterable: QIterable[Fraction]) -> QFractionIterable: return cast(QFractionIterable, iterable)
    def _selfcast_ordered(self, iterable: QOrderedIterable[Fraction]) -> QFractionOrderedIterable: return cast(QFractionOrderedIterable, iterable)

    # region override methods so that typecheckers know that we actually return QFractionIterables now, not QIterable[Fraction]
    # call the base method to eliminate code duplication. The base class will call lazy from just above, so it is already the correct type
    @override
    def where(self, predicate: Predicate[Fraction]) -> QFractionIterable: return self._selfcast(super().where(predicate))
    @override
    def where_not_none(self) -> QFractionIterable: return self._selfcast(super().where_not_none())
    @override
    def distinct(self) -> QFractionIterable: return self._selfcast(super().distinct())
    @override
    def distinct_by[TKey](self, key_selector: Selector[Fraction, TKey]) -> QFractionIterable: return self._selfcast(super().distinct_by(key_selector))
    @override
    def take(self, count: int) -> QFractionIterable: return self._selfcast(super().take(count))
    @override
    def take_while(self, predicate: Predicate[Fraction]) -> QFractionIterable: return self._selfcast(super().take_while(predicate))
    @override
    def take_last(self, count: int) -> QFractionIterable: return self._selfcast(super().take_last(count))
    @override
    def skip(self, count: int) -> QFractionIterable: return self._selfcast(super().skip(count))
    @override
    def skip_last(self, count: int) -> QFractionIterable: return self._selfcast(super().skip_last(count))
    @override
    def reversed(self) -> QFractionIterable: return self._selfcast(super().reversed())

    @override
    def concat(self, *others: Iterable[Fraction]) -> QFractionIterable: return self._selfcast(super().concat(*others))

    @override
    def order_by(self, key_selector: Selector[Fraction, SupportsRichComparison]) -> QFractionOrderedIterable: return self._selfcast_ordered(super().order_by(key_selector))
    @override
    def order_by_descending(self, key_selector: Selector[Fraction, SupportsRichComparison]) -> QFractionOrderedIterable: return self._selfcast_ordered(super().order_by_descending(key_selector))
    # endregion

    @override
    def to_list(self) -> QFractionList: return QFractionList(self)

    @override
    def to_sequence(self) -> QFractionSequence: return QFractionSequence(self)

    @override
    def to_set(self) -> QFractionSet: return QFractionSet(self)

    @override
    def to_frozenset(self) -> QFractionFrozenSet: return QFractionFrozenSet(self)

class QFractionIterableImplementation(QLazyIterableImplementation[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[Fraction]]) -> None:
        super().__init__(factory)

class QFractionOrderedIterable(QOrderedIterable[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[Fraction]], sorting_instructions: list[SortInstruction[Fraction]]) -> None:
        super().__init__(factory, sorting_instructions)

class QFractionList(QList[Fraction], QFractionIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[Fraction] = ()) -> None:
        super().__init__(iterable)

    @override
    def reversed(self) -> QFractionIterable: return QFractionIterable.reversed(self)

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

    @override
    def reversed(self) -> QFractionIterable: return QFractionIterable.reversed(self)
