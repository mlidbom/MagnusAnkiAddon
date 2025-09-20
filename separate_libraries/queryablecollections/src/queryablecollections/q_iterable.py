from __future__ import annotations

from abc import ABC
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any, overload

from queryablecollections._private_implementation_details import q_ops_bool, q_ops_filtering, q_ops_grouping, q_ops_loop, q_ops_ordering, q_ops_single_elements, q_ops_transform
from queryablecollections._private_implementation_details.q_ops_ordering import SortInstruction

# noinspection PyPep8Naming
from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadCollectionConstructors as C
from queryablecollections.q_errors import EmptyIterableError

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

    from queryablecollections._private_implementation_details.type_aliases import Action1, Predicate, Selector
    from queryablecollections.collections.q_frozen_set import QFrozenSet
    from queryablecollections.collections.q_list import QList
    from queryablecollections.collections.q_sequence import QSequence
    from queryablecollections.collections.q_set import QSet
    from queryablecollections.q_cast import QCast
    from queryablecollections.q_grouping import QGrouping
    from queryablecollections.q_ordered_iterable import QOrderedIterable

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return C.iterable(value)

class QIterable[TItem](Iterable[TItem], ABC):
    __slots__: tuple[str, ...] = ()
    @staticmethod
    def create(value: Iterable[TItem]) -> QIterable[TItem]: return C.iterable(value)

    @property
    def cast(self) -> QCast[TItem]: return C.cast(self)

    # region operations on the whole collection, not the items
    def concat(self, *others: Iterable[TItem]) -> QIterable[TItem]: return C.iterable(q_ops_transform.concat(self, *others))
    # endregion

    # region functional programming helpers
    def pipe_to[TReturn](self, action: Selector[QIterable[TItem], TReturn]) -> TReturn: return action(self)
    # endregion

    # region filtering
    def where(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return C.iterable(q_ops_filtering.where(self, predicate))
    def where_not_none(self) -> QIterable[TItem]: return C.iterable(q_ops_filtering.where_not_none(self))

    def distinct(self) -> QIterable[TItem]: return C.lazy_iterable(lambda: q_ops_filtering.distinct(self))

    def take_while(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return C.iterable(q_ops_filtering.take_while(self, predicate))
    def take(self, count: int) -> QIterable[TItem]: return C.iterable(q_ops_filtering.take(self, count))
    def take_last(self, count: int) -> QIterable[TItem]: return C.lazy_iterable(lambda: q_ops_filtering.take_last(self, count))
    def skip(self, count: int) -> QIterable[TItem]: return C.iterable(q_ops_filtering.skip(self, count))
    def skip_last(self, count: int) -> QIterable[TItem]: return C.lazy_iterable(lambda: q_ops_filtering.skip_last(self, count))
    # endregion

    # region scalar aggregations
    def qcount(self, predicate: Predicate[TItem] | None = None) -> int:
        if predicate is not None: return self.where(predicate).qcount()
        return self._optimized_length()

    def _optimized_length(self) -> int: return sum(1 for _ in self)

    # endregion

    # region sorting
    def order_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        from queryablecollections.q_ordered_iterable import QOrderedIterable
        return QOrderedIterable(self, [SortInstruction(key_selector, False)])

    def order_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        from queryablecollections.q_ordered_iterable import QOrderedIterable
        return QOrderedIterable(self, [SortInstruction(key_selector, True)])

    def reversed(self) -> QIterable[TItem]: return C.lazy_iterable(q_ops_ordering.reverse_lazy(self))

    def ordered(self) -> QIterable[TItem]:
        return C.lazy_iterable(lambda: q_ops_ordering.ordered(self))  # pyright: ignore [reportUnknownArgumentType, reportArgumentType, reportUnknownLambdaType]
    # endregion

    # region boolean queries
    def none(self, predicate: Predicate[TItem] | None = None) -> bool: return not q_ops_bool.any_(self, predicate)
    def any(self, predicate: Predicate[TItem] | None = None) -> bool: return q_ops_bool.any_(self, predicate)
    def all(self, predicate: Predicate[TItem]) -> bool: return q_ops_bool.all_(self, predicate)
    # endregion

    # region mapping/transformation methods
    def select[TReturn](self, selector: Selector[TItem, TReturn]) -> QIterable[TReturn]: return C.iterable(q_ops_transform.select(self, selector))
    def select_many[TInner](self, selector: Selector[TItem, Iterable[TInner]]) -> QIterable[TInner]: return C.iterable(q_ops_transform.select_many(self, selector))

    def zip[TOther, TResult](self, other: Iterable[TOther], selector: Callable[[TItem, TOther], TResult]) -> QIterable[TResult]:
        return C.iterable(q_ops_transform.zip_with_selector(self, other, selector))

    def join[TInner, TKey, TResult](self, inner: Iterable[TInner], outer_key: Selector[TItem, TKey], inner_key: Selector[TInner, TKey], result: Callable[[TItem, TInner], TResult]) -> QIterable[TResult]:
        return C.iterable(q_ops_transform.join(self, inner, outer_key, inner_key, result))

    @overload
    def group_by[TKey](self, key: Selector[TItem, TKey]) -> QIterable[QGrouping[TKey, TItem]]:
        """Groups the elements of a sequence according to the specified key selector"""

    @overload
    def group_by[TKey, TElement](self, key: Selector[TItem, TKey], element: Selector[TItem, TElement]) -> QIterable[QGrouping[TKey, TElement]]:
        """Groups the elements of a sequence according to the specified key selector and element selector"""

    def group_by[TKey, TElement](self, key: Selector[TItem, TKey], element: Selector[TItem, TElement] | None = None) -> QIterable[QGrouping[TKey, TItem]] | QIterable[QGrouping[TKey, TElement]]:
        return (C.iterable(q_ops_grouping.group_by(self, key))
                if element is None
                else C.iterable(q_ops_grouping.group_by_with_element_selector(self, key, element)))
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
    def to_list(self) -> QList[TItem]: return C.list(self)
    def to_set(self) -> QSet[TItem]: return C.set(self)
    def to_frozenset(self) -> QFrozenSet[TItem]: return C.frozen_set(self)
    def to_sequence(self) -> QSequence[TItem]: return C.sequence(self)
    def to_built_in_list(self) -> list[TItem]: return list(self)
    # endregion

    @staticmethod
    def empty() -> QIterable[TItem]: return C.empty_iterable()

# region implementing classes
