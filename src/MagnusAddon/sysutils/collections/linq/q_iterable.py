from __future__ import annotations

import itertools
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, cast, override

from ex_autoslot import AutoSlotsABC

if TYPE_CHECKING:
    from collections.abc import Iterator

    from _typeshed import SupportsRichComparison
    from sysutils.standard_type_aliases import Action1, Func, Predicate, Selector

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(value)

class QIterable[TItem](Iterable[TItem], AutoSlotsABC):
    @staticmethod
    def create(value: Iterable[TItem]) -> QIterable[TItem]: return _Qiterable(value)

    # region queries that need to be static so that we can know the type of the the LLitearble

    # region operations on the whole collection, not the items
    def pipe_to[TReturn](self, action: Selector[QIterable[TItem], TReturn]) -> TReturn:
        return action(self)
    # endregion

    # region filtering
    def where(self, predicate: Predicate[TItem]) -> QIterable[TItem]:
        return _Qiterable(item for item in self if predicate(item))

    def where_not_none(self) -> QIterable[TItem]:
        return self.where(lambda item: item is not None)

    def unique(self) -> QIterable[TItem]:
        return _LazyQiterable(lambda: dict.fromkeys(self))

    def take_while(self, predicate: Predicate[TItem]) -> QIterable[TItem]:
        return _Qiterable(itertools.takewhile(predicate, self))

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

    def reversed(self) -> QIterable[TItem]:
        return _LazyQiterable[TItem](lambda: reversed(self.to_built_in_list()))
    # endregion

    # region boolean queries
    def none(self, predicate: Predicate[TItem] | None = None) -> bool: return not self.any(predicate)

    def any(self, predicate: Predicate[TItem] | None = None) -> bool:
        if predicate is None:
            for _ in self: return True
            return False
        return any(predicate(item) for item in self)

    def all(self, predicate: Predicate[TItem]) -> bool:
        return not self.any(lambda item: not predicate(item))
    # endregion

    # region mapping methods
    def select[TReturn](self, selector: Selector[TItem, TReturn]) -> QIterable[TReturn]:
        return _Qiterable(selector(item) for item in self)

    def select_many[TInner](self, selector: Selector[TItem, Iterable[TInner]]) -> QIterable[TInner]:
        return _Qiterable(itertools.chain.from_iterable(selector(item) for item in self))
    # endregion

    # region single item selecting methods
    def single(self, predicate: Predicate[TItem] | None = None) -> TItem:
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

    def single_or_none(self, predicate: Predicate[TItem] | None = None) -> TItem | None:
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
    def assert_each(self, predicate: Predicate[TItem], message: str | None = None) -> QIterable[TItem]:
        for item in self:
            if not predicate(item): raise AssertionError(message or "")
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
    # endregion

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
class SortInstruction[TItem]:
    def __init__(self, key_selector: Selector[TItem, SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Selector[TItem, SupportsRichComparison] = key_selector
        self.descending: bool = descending

class QOrderedIterable[TItem](QIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem], sorting_instructions: list[SortInstruction[TItem]]) -> None:
        self.sorting_instructions: list[SortInstruction[TItem]] = sorting_instructions
        self._unsorted: Iterable[TItem] = iterable

    def then_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=False)])

    def then_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=True)])

    @override
    def __iter__(self) -> Iterator[TItem]:
        items = list(self._unsorted)
        for instruction in self.sorting_instructions:
            items.sort(key=instruction.key_selector, reverse=instruction.descending)

        yield from items
# endregion

# region LList, LSet, LFrozenSet: concrete classes that do very little but inherit a built in collection and LIterable and provide an override or two for performance
class QList[TItem](list[TItem], QIterable[TItem], AutoSlotsABC):
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return _LazyQiterable[TItem](lambda: reversed(self))

    @override
    def element_at(self, index: int) -> TItem: return self[index]

class QFrozenSet[TItem](frozenset[TItem], QIterable[TItem], AutoSlotsABC):
    def __new__(cls, iterable: Iterable[TItem] = ()) -> QFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

class QSet[TItem](set[TItem], QIterable[TItem], AutoSlotsABC):
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)
# endregion
# endregion
