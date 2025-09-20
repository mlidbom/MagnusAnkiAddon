from __future__ import annotations

from abc import ABC
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any, overload

import queryablecollections._private_implementation_details.operations as ops

# noinspection PyPep8Naming
from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

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

# note to coders, you can trust that the methods in QIterable do nothing except delegate to the corresponding operations method,
# or to ZeroImportOverheadConstructors, that's why we keep all the methods on single lines to make it easier to read through the definitions
class QIterable[TItem](Iterable[TItem], ABC):
    __slots__: tuple[str, ...] = ()
    @property
    def cast(self) -> QCast[TItem]: return C.cast(self)

    # region operations on the whole collection, not the items
    def concat(self, *others: Iterable[TItem]) -> QIterable[TItem]: return ops.transforms.concat(self, *others)
    # endregion

    # region functional programming helpers
    def pipe_to[TReturn](self, action: Selector[QIterable[TItem], TReturn]) -> TReturn: return ops.functional.pipe_to(self, action)
    def for_each(self, action: Action1[TItem]) -> QIterable[TItem]: return ops.functional.for_each(self, action)
    def for_single(self, action: Selector[TItem, Any]) -> QIterable[TItem]:  return ops.functional.for_single(self, action)  # pyright: ignore[reportExplicitAny]
    def for_single_or_none(self, action: Selector[TItem, Any]) -> QIterable[TItem]: return ops.functional.for_single_or_none(self, action)  # pyright: ignore[reportExplicitAny]
    # endregion

    # region filtering
    def where(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return ops.filtering.where(self, predicate)
    def where_not_none(self) -> QIterable[TItem]: return ops.filtering.where_not_none(self)

    def distinct(self) -> QIterable[TItem]: return ops.filtering.distinct(self)

    def take_while(self, predicate: Predicate[TItem]) -> QIterable[TItem]: return ops.filtering.take_while(self, predicate)
    def take(self, count: int) -> QIterable[TItem]: return ops.filtering.take(self, count)
    def take_last(self, count: int) -> QIterable[TItem]: return ops.filtering.take_last(self, count)
    def skip(self, count: int) -> QIterable[TItem]: return ops.filtering.skip(self, count)
    def skip_last(self, count: int) -> QIterable[TItem]: return ops.filtering.skip_last(self, count)
    # endregion

    # region value queries
    def qcount(self, predicate: Predicate[TItem] | None = None) -> int: return ops.scalars.count(self, predicate)
    def none(self, predicate: Predicate[TItem] | None = None) -> bool: return not ops.scalars.any_(self, predicate)
    def any(self, predicate: Predicate[TItem] | None = None) -> bool: return ops.scalars.any_(self, predicate)
    def all(self, predicate: Predicate[TItem]) -> bool: return ops.scalars.all_(self, predicate)

    # endregion

    # region sorting
    def order_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]: return ops.ordering.order_by(self, key_selector)
    def order_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]: return ops.ordering.order_by_descending(self, key_selector)

    def reversed(self) -> QIterable[TItem]: return ops.ordering.reverse_lazy(self)

    def ordered(self) -> QIterable[TItem]: return ops.ordering.ordered(self)  # pyright: ignore [reportUnknownVariableType, reportArgumentType]
    # endregion

    # region mapping/transformation methods
    def select[TReturn](self, selector: Selector[TItem, TReturn]) -> QIterable[TReturn]: return ops.transforms.select(self, selector)
    def select_many[TInner](self, selector: Selector[TItem, Iterable[TInner]]) -> QIterable[TInner]: return ops.transforms.select_many(self, selector)
    def zip[TOther, TResult](self, other: Iterable[TOther], selector: Callable[[TItem, TOther], TResult]) -> QIterable[TResult]: return ops.transforms.zip_with_selector(self, other, selector)
    def join[TInner, TKey, TResult](self, inner: Iterable[TInner], outer_key: Selector[TItem, TKey], inner_key: Selector[TInner, TKey], result: Callable[[TItem, TInner], TResult]) -> QIterable[TResult]: return ops.transforms.join(self, inner, outer_key, inner_key, result)

    @overload
    def group_by[TKey](self, key: Selector[TItem, TKey]) -> QIterable[QGrouping[TKey, TItem]]:
        """Groups the elements of a sequence according to the specified key selector"""

    @overload
    def group_by[TKey, TElement](self, key: Selector[TItem, TKey], element: Selector[TItem, TElement]) -> QIterable[QGrouping[TKey, TElement]]:
        """Groups the elements of a sequence according to the specified key selector and element selector"""

    def group_by[TKey, TElement](self, key: Selector[TItem, TKey], element: Selector[TItem, TElement] | None = None) -> QIterable[QGrouping[TKey, TItem]] | QIterable[QGrouping[TKey, TElement]]: return ops.grouping.group_by_q(self, key, element)
    # endregion

    # region single item selecting methods
    def first(self, predicate: Predicate[TItem] | None = None) -> TItem: return ops.single_elements.first(self, predicate)
    def first_or_none(self, predicate: Predicate[TItem] | None = None) -> TItem | None: return ops.single_elements.first_or_none(self, predicate)
    def single(self, predicate: Predicate[TItem] | None = None) -> TItem: return ops.single_elements.single(self, predicate)
    def single_or_none(self, predicate: Predicate[TItem] | None = None) -> TItem | None: return ops.single_elements.single_or_none(self, predicate)

    def element_at(self, index: int) -> TItem: return ops.single_elements.element_at(self, index)
    def element_at_or_none(self, index: int) -> TItem | None: return ops.single_elements.element_at_or_none(self, index)
    # endregion

    # region assertions on the collection or it's values
    def assert_each(self, predicate: Predicate[TItem], message: str | Selector[TItem, str] | None = None) -> QIterable[TItem]: return ops.asserts.each_element(self, predicate, message)
    def assert_on_collection(self, predicate: Predicate[QIterable[TItem]], message: str | None = None) -> QIterable[TItem]: return ops.asserts.collection(self, predicate, message)
    # endregion

    # region methods subclasses may want to override for perfarmonce reasons

    def _optimized_length(self) -> int: return sum(1 for _ in self)
    def _assert_not_empty(self) -> QIterable[TItem]: return ops.asserts.not_empty(self)

    # region factory methods
    # note: we do not "optimize" by returning self in any subclass because the contract is to create a new independent copy
    def to_list(self) -> QList[TItem]: return C.list(self)
    def to_set(self) -> QSet[TItem]: return C.set(self)
    def to_frozenset(self) -> QFrozenSet[TItem]: return C.frozen_set(self)
    def to_sequence(self) -> QSequence[TItem]: return C.sequence(self)
    def to_built_in_list(self) -> list[TItem]: return list(self)
    # endregion

    # endregion

    @staticmethod
    def empty() -> QIterable[TItem]: return C.empty_iterable()

# region implementing classes
