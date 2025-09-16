from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, cast, override

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from _typeshed import SupportsRichComparison

def linq[TItem](value: Iterable[TItem]) -> LIterable[TItem]: return _LIterable(value)

class LIterable[TItem](Iterable[TItem], ABC):
    @staticmethod
    def create(value: Iterable[TItem]) -> LIterable[TItem]: return _LIterable(value)

    # region filtering
    def where(self, predicate: Callable[[TItem], bool]) -> LIterable[TItem]:
        return _LIterable(item for item in self._value if predicate(item))

    def where_not_none(self) -> LIterable[TItem]:
        return self.where(lambda item: item is not None)

    def unique(self) -> LList[TItem]:
        return LList(dict.fromkeys(self._value))

    # endregion

    # region scalar aggregations
    def length(self) -> int:
        if isinstance(self, list): return len(cast(list[TItem], self))
        return sum(1 for _ in self)
    # endregion

    # region order_by
    def order_by(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedLIterable[TItem]:
        return LOrderedLIterable(self, [SortInstruction(key_selector, False)])

    def order_by_descending(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedLIterable[TItem]:
        return LOrderedLIterable(self, [SortInstruction(key_selector, True)])
    # endregion

    # region boolean queries
    def none(self, predicate: Callable[[TItem], bool] | None = None) -> bool: return not self.any(predicate)

    def any(self, predicate: Callable[[TItem], bool] | None = None) -> bool:
        if predicate is None:
            for _ in self: return True
            return False
        return any(predicate(item) for item in self)
    # endregion

    # region mapping methods
    def select[TReturn](self, selector: Callable[[TItem], TReturn]) -> LIterable[TReturn]:
        return _LIterable(selector(item) for item in self)

    def select_many[TInner](self, selector: Callable[[TItem], Iterable[TInner]]) -> LIterable[TInner]:
        return _LIterable(itertools.chain.from_iterable(selector(item) for item in self))
    # endregion

    # region single item selecting methods
    def single(self, predicate: Callable[[TItem], bool] | None = None) -> TItem:
        result = self.single_or_default(predicate)
        if result is None: raise ValueError("Sequence contains no elements")
        return result

    def single_or_default(self, predicate: Callable[[TItem], bool] | None = None) -> TItem | None:
        if predicate is None:
            iterator: Iterator[TItem] = iter(self._value)
            try:
                first: TItem = next(iterator)
                try:
                    next(iterator)  # Check if there's a second item
                    raise ValueError("Sequence contains more than one element")
                except StopIteration:
                    return first
            except StopIteration:
                return None
        return self.where(predicate).single_or_default()
    # endregion

    # region assertions on the collection or it's values
    def assert_each(self, predicate: Callable[[TItem], bool], message: str | None = None) -> LIterable[TItem]:
        for item in self:
            if not predicate(item): raise AssertionError(message)
        return self

    def reversed(self) -> LIterable[TItem]:
        return _LIterable[TItem](reversed(self.to_built_in_list()))

    def assert_on_collection(self, predicate: Callable[[LIterable[TItem]], bool], message: str | None = None) -> LIterable[TItem]:
        if not predicate(self): raise AssertionError(message)
        return self
    # endregion

    # region methods to avoid needing to manually write loops
    def for_each(self, action: Callable[[TItem], None]) -> LIterable[TItem]:
        for item in self._value: action(item)
        return self

    def for_single(self, action: Callable[[TItem], Any]) -> LIterable[TItem]:  # pyright: ignore[reportExplicitAny]
        action(self.single())
        return self

    def for_single_or_none(self, action: Callable[[TItem], Any]) -> LIterable[TItem]:  # pyright: ignore[reportExplicitAny]
        value = self.single_or_default()
        if value is not None: action(value)
        return self
    # endregion

    # region factory methods
    # note: we do not "optimize" by returning self in any subclass because the contract is to create a new independent copy
    def to_list(self) -> LList[TItem]: return LList(self)
    def to_built_in_list(self) -> list[TItem]: return list(self)
    def to_set(self) -> LSet[TItem]: return LSet(self)
    def to_frozenset(self) -> LFrozenSet[TItem]: return LFrozenSet(self)
    # endregion

    # region the abstract _value property
    @property
    @abstractmethod
    def _value(self) -> Iterable[TItem]: raise NotImplementedError()
    # endregion

# region implementing classes
class _LIterable[TItem](LIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self.__value: Iterable[TItem] = iterable

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self.__value

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value

# region LOrderedLIterable
class SortInstruction[TItem]:
    def __init__(self, key_selector: Callable[[TItem], SupportsRichComparison], descending: bool) -> None:
        self.key_selector = key_selector
        self.descending = descending

class LOrderedLIterable[TItem](LIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem], sorting_instructions: list[SortInstruction[TItem]]) -> None:
        self.sorting_instructions: list[SortInstruction[TItem]] = sorting_instructions
        self._unsorted: Iterable[TItem] = iterable

    def then_by(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedLIterable[TItem]:
        self.sorting_instructions.append(SortInstruction(key_selector, descending=False))
        return LOrderedLIterable(self._unsorted, self.sorting_instructions)

    def then_by_descending(self, key_selector: Callable[[TItem], SupportsRichComparison]) -> LOrderedLIterable[TItem]:
        self.sorting_instructions.append(SortInstruction(key_selector, descending=True))
        return LOrderedLIterable(self._unsorted, self.sorting_instructions)

    @property
    @override
    def _value(self) -> Iterable[TItem]:
        return self._l_ordered_iterable_sort()

    def _l_ordered_iterable_sort(self) -> list[TItem]:  # the name is so that the method is understandable in a profiling result that does not include the type
        items = list(self._unsorted)

        for instruction in self.sorting_instructions:
            items.sort(key=instruction.key_selector, reverse=instruction.descending)

        return items

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value
# endregion

# region LList, LSet, LFrozenSet: concrete classes that do very little but inherit a built in collection and LIterable and provide an override or two for performance
class LFrozenSet[TItem](frozenset[TItem], LIterable[TItem]):
    def __new__(cls, iterable: Iterable[TItem]) -> LFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self

    @override
    def length(self) -> int: return len(self)

class LList[TItem](list[TItem], LIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        super().__init__(iterable)

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self

    @override
    def length(self) -> int: return len(self)

    @override
    def reversed(self) -> LIterable[TItem]: return LList[TItem](reversed(self))

class LSet[TItem](set[TItem], LIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        super().__init__(iterable)

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self

    @override
    def length(self) -> int: return len(self)
# endregion
# endregion
