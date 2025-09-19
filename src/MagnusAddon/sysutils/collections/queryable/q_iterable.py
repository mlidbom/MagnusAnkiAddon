from __future__ import annotations

import itertools
import sys
from abc import ABC
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any, SupportsIndex, cast, overload, override

from ex_autoslot import AutoSlotsABC
from sysutils.collections.immutable_sequence import ImmutableSequence
from sysutils.collections.queryable import q_ops
from sysutils.collections.queryable.q_ops import SortInstruction

if TYPE_CHECKING:
    from collections.abc import Iterator

    from _typeshed import SupportsRichComparison
    from sysutils.standard_type_aliases import Action1, Func, Predicate, Selector

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(value)

class QIterable[TItem](Iterable[TItem], ABC, AutoSlotsABC):
    @staticmethod
    def create(value: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(value)

    # region queries that need to be static so that we can know the type of the the LLitearble

    # region operations on the whole collection, not the items
    def concat(self, other: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(q_ops.concat(self, other))
    def pipe_to[TReturn](self, action: Selector[QIterable[TItem], TReturn]) -> TReturn: return action(self)
    # endregion

    # region filtering
    def where(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return _Qiterable(q_ops.where(predicate, self))
    def where_not_none(self) -> QIterable[TItem]: return self.where(lambda item: item is not None)
    def distinct(self) -> QIterable[TItem]: return _LazyQiterable(lambda: q_ops.distinct(self))
    def take_while(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return _Qiterable(q_ops.take_while(predicate, self))

    # endregion

    # region scalar aggregations
    def length(self, predicate: Predicate[TItem] | None = None) -> int:
        if predicate is not None: return self.where(predicate).length()
        return self._optimized_length()

    def _optimized_length(self) -> int: return sum(1 for _ in self)

    # endregion

    # region sorting
    def order_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self, [SortInstruction(key_selector, False)])

    def order_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self, [SortInstruction(key_selector, True)])

    def reversed(self) -> QIterable[TItem]: return _LazyQiterable[TItem](lambda: reversed(self.to_built_in_list()))
    # endregion

    # region boolean queries
    def none(self, predicate: Predicate[TItem] | None = None) -> bool: return not q_ops.any_(self, predicate)
    def any(self, predicate: Predicate[TItem] | None = None) -> bool: return q_ops.any_(self, predicate)
    def all(self, predicate: Predicate[TItem]) -> bool: return not self.any(lambda item: not predicate(item))
    # endregion

    # region mapping methods
    def select[TReturn](self, selector: Selector[TItem, TReturn]) -> QIterable[TReturn]: return _Qiterable(q_ops.select(selector, self))
    def select_many[TInner](self, selector: Selector[TItem, Iterable[TInner]]) -> QIterable[TInner]: return _Qiterable(q_ops.select_many(self, selector))
    # endregion

    # region single item selecting methods
    def single(self, predicate: Predicate[TItem] | None = None) -> TItem: return q_ops.single(self, predicate)

    def single_or_none(self, predicate: Predicate[TItem] | None = None) -> TItem | None:
        if predicate is None: return q_ops.single_or_none(self)
        return self.where(predicate).single_or_none()

    def element_at(self, index: int) -> TItem:
        try:
            return next(itertools.islice(self, index, index + 1))
        except StopIteration:
            raise IndexError(f"Index {index} was outside the bounds of the collection.") from None

    def element_at_or_default(self, index: int) -> TItem | None:
        return next(itertools.islice(self, index, index + 1), None)

    # endregion

    # region assertions on the collection or it's values
    def assert_each(self, predicate: Predicate[TItem], message: str | Selector[TItem, str] | None = None) -> QIterable[TItem]:
        for item in self:
            actual_message = message if isinstance(message, str) else message(item) if message is not None else ""
            if not predicate(item): raise AssertionError(actual_message)
        return self

    def assert_on_collection(self, predicate: Predicate[QIterable[TItem]], message: str | None = None) -> QIterable[TItem]:
        if not predicate(self): raise AssertionError(message)
        return self
    # endregion

    # region methods to avoid needing to manually write loops
    def for_each(self, action: Action1[TItem]) -> QIterable[TItem]:
        for item in self: action(item)
        return self

    def for_single(self, action: Selector[TItem, Any]) -> QIterable[TItem]:  # pyright: ignore[reportExplicitAny]
        action(self.single())
        return self

    def for_single_or_none(self, action: Selector[TItem, Any]) -> QIterable[TItem]:  # pyright: ignore[reportExplicitAny]
        value = self.single_or_none()
        if value is not None: action(value)
        return self
    # endregion

    # region factory methods
    # note: we do not "optimize" by returning self in any subclass because the contract is to create a new independent copy
    def to_list(self) -> QList[TItem]: return QList(self)
    def to_built_in_list(self) -> list[TItem]: return list(self)
    def to_set(self) -> QSet[TItem]: return QSet(self)
    def to_frozenset(self) -> QFrozenSet[TItem]: return QFrozenSet(self)
    def to_sequence(self) -> QSequence[TItem]: return QImmutableSequence(list(self))
    # endregion

    _empty_iterable: QIterable[TItem]
    @staticmethod
    def empty() -> QIterable[TItem]:
        return cast(QIterable[TItem], QIterable._empty_iterable)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QIterable can serve or any QIterable type in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

# region implementing classes
class _Qiterable[TItem](QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self._value: Iterable[TItem] = iterable

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value

class _LazyQiterable[TItem](QIterable[TItem]):
    def __init__(self, iterable_factory: Func[Iterable[TItem]]) -> None:
        self._factory: Func[Iterable[TItem]] = iterable_factory

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._factory()

# region LOrderedLIterable

class QOrderedIterable[TItem](QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem], sorting_instructions: list[SortInstruction[TItem]]) -> None:
        self.sorting_instructions: list[SortInstruction[TItem]] = sorting_instructions
        self._unsorted: Iterable[TItem] = iterable

    def then_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=False)])

    def then_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=True)])

    @override
    def __iter__(self) -> Iterator[TItem]: yield from q_ops.sort_by_instructions(self._unsorted, self.sorting_instructions)
# endregion


class QSequence[TItem](Sequence[TItem], QIterable[TItem], ABC, AutoSlotsABC):
    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return _LazyQiterable[TItem](lambda: reversed(self))

    _empty_sequence: QSequence[TItem]
    @override
    @staticmethod
    def empty() -> QSequence[TItem]:
        return cast(QSequence[TItem], QSequence._empty_sequence)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QList can serve as any QList in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

class QImmutableSequence[TItem](ImmutableSequence[TItem], QSequence[TItem]):
    def __init__(self, sequence: Sequence[TItem] = ()) -> None:
        super().__init__(sequence)

    @overload
    def __getitem__(self, index: int) -> TItem: ...
    @overload
    def __getitem__(self, index: slice) -> QImmutableSequence[TItem]: ...
    @override
    def __getitem__(self, index: int | slice) -> TItem | QImmutableSequence[TItem]:
        if isinstance(index, slice):
            return QImmutableSequence(super().__getitem__(index))
        return super().__getitem__(index)

# region LList, LSet, LFrozenSet: concrete classes
class QList[TItem](list[TItem], QSequence[TItem], QIterable[TItem], AutoSlotsABC):
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return _LazyQiterable[TItem](lambda: reversed(self))

    @override
    def element_at(self, index: int) -> TItem: return self[index]

    @override
    def index(self, value: TItem, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize) -> int:
        return super().index(value, start, stop)

    @override
    def count(self, value: TItem): return super().count(value)

    @overload
    def __getitem__(self, index: SupportsIndex) -> TItem: ...

    @overload
    def __getitem__(self, index: slice) -> QList[TItem]: ...

    @override
    def __getitem__(self, index: SupportsIndex | slice) -> TItem | QList[TItem]:
        if isinstance(index, slice):
            return QList(super().__getitem__(index))
        return super().__getitem__(index)

    @staticmethod
    @override
    def empty() -> QList[TItem]: return QList()  # QList is mutable, so unlike our base types we cannot reuse an instance

class QFrozenSet[TItem](frozenset[TItem], QIterable[TItem], AutoSlotsABC):
    def __new__(cls, iterable: Iterable[TItem] = ()) -> QFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    _empty_set: QFrozenSet[TItem]
    @override
    @staticmethod
    def empty() -> QFrozenSet[TItem]:
        return cast(QFrozenSet[TItem], QFrozenSet._empty_set)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QList can serve as any QList in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

class QSet[TItem](set[TItem], QIterable[TItem], AutoSlotsABC):
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    @staticmethod
    @override
    def empty() -> QSet[TItem]: return QSet()  # QSet is mutable, so unlike our base types we cannot reuse an instance

# an empty immutable Q* can serve or any Q* type in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost
QSequence._empty_sequence = QImmutableSequence()  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]
QIterable._empty_iterable = _Qiterable(())  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]
QFrozenSet._empty_set = QFrozenSet()  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]

# endregion
# endregion
