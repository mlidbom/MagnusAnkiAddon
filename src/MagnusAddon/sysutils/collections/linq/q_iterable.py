from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, cast, override

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from _typeshed import SupportsRichComparison

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(value)

class QIterable[TItem](Iterable[TItem], ABC):
    @staticmethod
    def create(value: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(value)

    # region queries that need to be static so that we can know the type of the the LLitearble

    # region operations on the whole collection, not the items
    def pipe_to[TReturn](self, action: Callable[[QIterable[TItem]], TReturn]) -> TReturn:
        return action(self)
    # endregion

    # region filtering
    def where(self, predicate: Callable[[TItem], bool]) -> QIterable[TItem]:
        return _Qiterable(item for item in self if predicate(item))

    def where_not_none(self) -> QIterable[TItem]:
        return self.where(lambda item: item is not None)

    def unique(self) -> QList[TItem]:
        return QList(dict.fromkeys(self))

    def take_while(self, predicate: Callable[[TItem], bool]) -> QIterable[TItem]:
        """`returns` an iterable containing the items in `iterable` until (exclusive) `condition` returns false"""
        return _Qiterable(itertools.takewhile(predicate, self))

    # endregion

    # region scalar aggregations
    def length(self) -> int:
        if isinstance(self, list): return len(cast(list[TItem], self))
        return sum(1 for _ in self)

    #todo: consider whether this is the best name. We need to avoid collisions with the built in count member, but...
    def length_where(self, predicate: Callable[[TItem], bool]) -> int:
        return self.where(predicate).length()

    # endregion

    # region order_by
    def order_by(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedQIterable[TItem]:
        return LOrderedQIterable(self, [SortInstruction(key_selector, False)])

    def order_by_descending(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedQIterable[TItem]:
        return LOrderedQIterable(self, [SortInstruction(key_selector, True)])
    # endregion

    # region boolean queries
    def none(self, predicate: Callable[[TItem], bool] | None = None) -> bool: return not self.any(predicate)

    def any(self, predicate: Callable[[TItem], bool] | None = None) -> bool:
        if predicate is None:
            for _ in self: return True
            return False
        return any(predicate(item) for item in self)

    def all(self, predicate: Callable[[TItem], bool]) -> bool:
        return not self.any(lambda item: not predicate(item))
    # endregion

    # region mapping methods
    def select[TReturn](self, selector: Callable[[TItem], TReturn]) -> QIterable[TReturn]:
        return _Qiterable(selector(item) for item in self)

    def select_many[TInner](self, selector: Callable[[TItem], Iterable[TInner]]) -> QIterable[TInner]:
        return _Qiterable(itertools.chain.from_iterable(selector(item) for item in self))
    # endregion

    # region single item selecting methods
    def single(self, predicate: Callable[[TItem], bool] | None = None) -> TItem:
        if not predicate:
            first: TItem | None = None
            found = False
            for current_index, item in enumerate(self):
                if current_index > 0:
                    raise ValueError("Sequence contains more than one element")
                first = item
                found = True
            if found: return cast(TItem, first)
            raise IndexError("Index 0 was outside the bounds of the collection.")

        return self.where(predicate).single()

    def single_or_none(self, predicate: Callable[[TItem], bool] | None = None) -> TItem | None:
        if predicate is None:
            first: TItem | None = None
            for current_index, item in enumerate(self):
                if current_index > 0:
                    raise ValueError("Sequence contains more than one element")
                first = item
            return first

        return self.where(predicate).single_or_none()

    def element_at(self, index: int) -> TItem:
        for current_index, item in enumerate(self):
            if current_index == index:
                return item
        raise IndexError(f"Index {index} was outside the bounds of the collection.")

    # endregion

    # region assertions on the collection or it's values
    def assert_each(self, predicate: Callable[[TItem], bool], message: str | None = None) -> QIterable[TItem]:
        for item in self:
            if not predicate(item): raise AssertionError(message)
        return self

    def reversed(self) -> QIterable[TItem]:
        return _Qiterable[TItem](reversed(self.to_built_in_list()))

    def assert_on_collection(self, predicate: Callable[[QIterable[TItem]], bool], message: str | None = None) -> QIterable[TItem]:
        if not predicate(self): raise AssertionError(message)
        return self
    # endregion

    # region methods to avoid needing to manually write loops
    def for_each(self, action: Callable[[TItem], None]) -> QIterable[TItem]:
        for item in self: action(item)
        return self

    def for_single(self, action: Callable[[TItem], Any]) -> QIterable[TItem]:  # pyright: ignore[reportExplicitAny]
        action(self.single())
        return self

    def for_single_or_none(self, action: Callable[[TItem], Any]) -> QIterable[TItem]:  # pyright: ignore[reportExplicitAny]
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
    # endregion

# region implementing classes
class _Qiterable[TItem](QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self._value: Iterable[TItem] = iterable

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value

# region LOrderedLIterable
class SortInstruction[TItem]:
    def __init__(self, key_selector: Callable[[TItem], SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Callable[[TItem], SupportsRichComparison] = key_selector
        self.descending: bool = descending

class LOrderedQIterable[TItem](QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem], sorting_instructions: list[SortInstruction[TItem]]) -> None:
        self.sorting_instructions: list[SortInstruction[TItem]] = sorting_instructions
        self._unsorted: Iterable[TItem] = iterable

    def then_by(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedQIterable[TItem]:
        self.sorting_instructions.append(SortInstruction(key_selector, descending=False))
        return LOrderedQIterable(self._unsorted, self.sorting_instructions)

    def then_by_descending(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedQIterable[TItem]:
        self.sorting_instructions.append(SortInstruction(key_selector, descending=True))
        return LOrderedQIterable(self._unsorted, self.sorting_instructions)

    def _l_ordered_iterable_sort(self) -> list[TItem]:  # the name is so that the method is understandable in a profiling result that does not include the type
        items = list(self._unsorted)

        for instruction in self.sorting_instructions:
            items.sort(key=instruction.key_selector, reverse=instruction.descending)

        return items

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._l_ordered_iterable_sort()
# endregion

# region LList, LSet, LFrozenSet: concrete classes that do very little but inherit a built in collection and LIterable and provide an override or two for performance
class QList[TItem](list[TItem], QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return QList[TItem](reversed(self))

    @override
    def element_at(self, index: int) -> TItem: return self[index]

class QFrozenSet[TItem](frozenset[TItem], QIterable[TItem]):
    def __new__(cls, iterable: Iterable[TItem]) -> QFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @override
    def length(self) -> int: return len(self)

class QSet[TItem](set[TItem], QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def length(self) -> int: return len(self)
# endregion
# endregion
