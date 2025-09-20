from __future__ import annotations

from abc import ABC
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, cast, overload, override

from queryablecollections.empty_iterable_exception import EmptyIterableError
from queryablecollections.operations import q_ops_bool, q_ops_filtering, q_ops_grouping, q_ops_loop, q_ops_ordering, q_ops_single_elements, q_ops_transform
from queryablecollections.operations.q_ops_ordering import SortInstruction

if TYPE_CHECKING:
    from collections.abc import Iterator

    from _typeshed import SupportsRichComparison
    from queryablecollections.collections.q_frozen_set import QFrozenSet
    from queryablecollections.collections.q_list import QList
    from queryablecollections.collections.q_sequence import QSequence
    from queryablecollections.collections.q_set import QSet
    from queryablecollections.q_cast import QCast
    from queryablecollections.q_grouping import QGrouping
    from queryablecollections.type_aliases import Action1, Func, Predicate, Selector

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return QiterableImplementation(value)

class QIterable[TItem](Iterable[TItem], ABC):
    __slots__: tuple[str, ...] = ()
    @staticmethod
    def create(value: Iterable[TItem]) -> QIterable[TItem]: return QiterableImplementation(value)

    @property
    def cast(self) -> QCast[TItem]:
        from queryablecollections.q_cast import QCast
        return QCast[TItem](self)

    # region operations on the whole collection, not the items
    def concat(self, *others: Iterable[TItem]) -> QIterable[TItem]: return QiterableImplementation(q_ops_transform.concat(self, *others))
    # endregion

    # region functional programming helpers
    def pipe_to[TReturn](self, action: Selector[QIterable[TItem], TReturn]) -> TReturn: return action(self)
    # endregion

    # region filtering
    def where(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return QiterableImplementation(q_ops_filtering.where(self, predicate))
    def where_not_none(self) -> QIterable[TItem]: return QiterableImplementation(q_ops_filtering.where_not_none(self))

    def distinct(self) -> QIterable[TItem]: return QLazyiterable(lambda: q_ops_filtering.distinct(self))

    def take_while(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return QiterableImplementation(q_ops_filtering.take_while(self, predicate))
    def take(self, count: int) -> QIterable[TItem]: return QiterableImplementation(q_ops_filtering.take(self, count))
    def take_last(self, count: int) -> QIterable[TItem]: return QLazyiterable(lambda: q_ops_filtering.take_last(self, count))
    def skip(self, count: int) -> QIterable[TItem]: return QiterableImplementation(q_ops_filtering.skip(self, count))
    def skip_last(self, count: int) -> QIterable[TItem]: return QLazyiterable(lambda: q_ops_filtering.skip_last(self, count))
    # endregion

    # region scalar aggregations
    def qcount(self, predicate: Predicate[TItem] | None = None) -> int:
        if predicate is not None: return self.where(predicate).qcount()
        return self._optimized_length()

    def _optimized_length(self) -> int: return sum(1 for _ in self)

    # endregion

    # region sorting
    def order_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self, [SortInstruction(key_selector, False)])

    def order_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self, [SortInstruction(key_selector, True)])

    def reversed(self) -> QIterable[TItem]: return QLazyiterable[TItem](q_ops_ordering.reverse_lazy(self))

    def ordered(self) -> QIterable[TItem]:
        return QLazyiterable(lambda: q_ops_ordering.ordered(self))  # pyright: ignore [reportUnknownArgumentType, reportArgumentType, reportUnknownLambdaType]
    # endregion

    # region boolean queries
    def none(self, predicate: Predicate[TItem] | None = None) -> bool: return not q_ops_bool.any_(self, predicate)
    def any(self, predicate: Predicate[TItem] | None = None) -> bool: return q_ops_bool.any_(self, predicate)
    def all(self, predicate: Predicate[TItem]) -> bool: return q_ops_bool.all_(self, predicate)
    # endregion

    # region mapping methods
    def select[TReturn](self, selector: Selector[TItem, TReturn]) -> QIterable[TReturn]: return QiterableImplementation(q_ops_transform.select(self, selector))
    def select_many[TInner](self, selector: Selector[TItem, Iterable[TInner]]) -> QIterable[TInner]: return QiterableImplementation(q_ops_transform.select_many(self, selector))
    # endregion

    # region grouping

    @overload
    def group_by[TKey](self, key: Selector[TItem, TKey]) -> QIterable[QGrouping[TKey, TItem]]:
        """Groups the elements of a sequence according to the specified key selector"""

    @overload
    def group_by[TKey, TElement](self, key: Selector[TItem, TKey], element: Selector[TItem, TElement]) -> QIterable[QGrouping[TKey, TElement]]:
        """Groups the elements of a sequence according to the specified key selector and element selector"""

    def group_by[TKey, TElement](self, key: Selector[TItem, TKey], element: Selector[TItem, TElement] | None = None) -> QIterable[QGrouping[TKey, TItem]] | QIterable[QGrouping[TKey, TElement]]:
        return (QiterableImplementation(q_ops_grouping.group_by(self, key))
                if element is None
                else QiterableImplementation(q_ops_grouping.group_by_with_element_selector(self, key, element)))
    # endregion

    # region single item selecting methods
    def first(self, predicate: Predicate[TItem] | None = None) -> TItem: return q_ops_single_elements.first(self, predicate)
    def first_or_none(self, predicate: Predicate[TItem] | None = None) -> TItem | None: return q_ops_single_elements.first_or_none(self, predicate)
    def single(self, predicate: Predicate[TItem] | None = None) -> TItem: return q_ops_single_elements.single(self, predicate)
    def single_or_none(self, predicate: Predicate[TItem] | None = None) -> TItem | None: return q_ops_single_elements.single_or_none(self, predicate)

    def element_at(self, index: int) -> TItem: return q_ops_single_elements.element_at(self, index)
    def element_at_or_none(self, index: int) -> TItem | None: return q_ops_single_elements.element_at_or_none(self, index)

    def _assert_not_empty(self) -> QIterable[TItem]:
        if self.none(): raise EmptyIterableError()
        return self

    # endregion

    # region assertions on the collection or it's values
    def assert_each(self, predicate: Predicate[TItem], message: str | Selector[TItem, str] | None = None) -> QIterable[TItem]:
        q_ops_loop.assert_each(self, predicate, message)
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
    def to_list(self) -> QList[TItem]:
        from queryablecollections.collections.q_list import QList
        return QList(self)
    def to_set(self) -> QSet[TItem]:
        from queryablecollections.collections.q_set import QSet
        return QSet(self)
    def to_frozenset(self) -> QFrozenSet[TItem]:
        from queryablecollections.collections.q_frozen_set import QFrozenSet
        return QFrozenSet(self)
    def to_sequence(self) -> QSequence[TItem]:
        from queryablecollections.collections.q_sequence import QImmutableSequence
        return QImmutableSequence(list(self))
    def to_built_in_list(self) -> list[TItem]: return list(self)
    # endregion

    _empty_iterable: QIterable[TItem]
    @staticmethod
    def empty() -> QIterable[TItem]:
        return cast(QIterable[TItem], QIterable._empty_iterable)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QIterable can serve or any QIterable type in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

# region implementing classes
class QiterableImplementation[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("_value",)
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self._value: Iterable[TItem] = iterable

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value

class QLazyiterable[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("_factory",)
    def __init__(self, iterable_factory: Func[Iterable[TItem]]) -> None:
        self._factory: Func[Iterable[TItem]] = iterable_factory

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._factory()

# region LOrderedLIterable

class QOrderedIterable[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("sorting_instructions", "_unsorted")
    def __init__(self, iterable: Iterable[TItem], sorting_instructions: list[SortInstruction[TItem]]) -> None:
        self.sorting_instructions: list[SortInstruction[TItem]] = sorting_instructions
        self._unsorted: Iterable[TItem] = iterable

    def then_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=False)])

    def then_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=True)])

    @override
    def __iter__(self) -> Iterator[TItem]: yield from q_ops_ordering.sort_by_instructions(self._unsorted, self.sorting_instructions)
# endregion


# region LList, LSet, LFrozenSet: concrete classes

# an empty immutable Q* can serve or any Q* type in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost
QIterable._empty_iterable = QiterableImplementation(())  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]

# endregion
# endregion
