from __future__ import annotations

from abc import ABC
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Self, overload

import queryablecollections._private_implementation_details.operations as ops
from queryablecollections._private_implementation_details.operations.ordering import SortInstruction

# noinspection PyPep8Naming
from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C
from queryablecollections.q_errors import EmptyIterableError

if TYPE_CHECKING:
    from decimal import Decimal
    from fractions import Fraction

    from _typeshed import SupportsRichComparison
    from queryablecollections._private_implementation_details.type_aliases import Action1, Func, Predicate, Selector
    from queryablecollections.collections.numeric.q_decimal_types import QDecimalIterable
    from queryablecollections.collections.numeric.q_float_types import QFloatIterable
    from queryablecollections.collections.numeric.q_fraction_types import QFractionIterable
    from queryablecollections.collections.numeric.q_int_types import QIntIterable
    from queryablecollections.collections.q_dict import QDict
    from queryablecollections.collections.q_frozen_set import QFrozenSet
    from queryablecollections.collections.q_list import QList
    from queryablecollections.collections.q_sequence import QSequence
    from queryablecollections.collections.q_set import QSet
    from queryablecollections.q_cast import QCast
    from queryablecollections.q_grouping import QGrouping
    from queryablecollections.q_ordered_iterable import QOrderedIterable

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return C.caching_iterable(value)

# note to coders, you can trust that the on single lines do nothing except delegate to the corresponding operations method,
# or to ZeroImportOverheadConstructors, knowing taht, keeping them on single lines to make it easier to read through the definitions
class QIterable[T](Iterable[T], ABC):
    __slots__: tuple[str, ...] = ()
    @property
    def cast(self) -> QCast[T]: return C.cast(self)

    def _lazy(self, factory: Func[Iterable[T]]) -> QIterable[T]:
        return C.lazy_iterable(factory)

    # region operations on the whole collection, not the items
    def concat(self, *others: Iterable[T]) -> QIterable[T]: return self._lazy(lambda: ops.transforms.concat(self, *others))
    # endregion

    # region functional programming helpers
    def pipe[TReturn](self, action: Selector[QIterable[T], TReturn]) -> TReturn: return ops.functional.pipe(self, action)
    def for_each(self, action: Action1[T]) -> Self:
        for item in self: action(item)
        return self
    # endregion

    # region typed convertions to access type specific functionality type checkers will only allow calls if the instance is the correct type

    def as_int_iterable(self: QIterable[int]) -> QIntIterable: return ops.transforms.as_int_iterable(self)
    def as_float_iterable(self: QIterable[float]) -> QFloatIterable: return ops.transforms.as_float_iterable(self)
    def as_fraction_iterable(self: QIterable[Fraction]) -> QFractionIterable: return ops.transforms.as_fraction_iterable(self)
    def as_decimal_iterable(self: QIterable[Decimal]) -> QDecimalIterable: return ops.transforms.as_decimal_iterable(self)

    # endregion

    # region filtering
    def where(self, predicate: Predicate[T]) -> QIterable[T]: return self._lazy(lambda: ops.filtering.where(self, predicate))
    def where_not_none(self) -> QIterable[T]: return self._lazy(lambda: ops.filtering.where_not_none(self))

    def distinct(self) -> QIterable[T]: return self._lazy(lambda: ops.filtering.distinct(self))

    def distinct_by[TKey](self, key_selector: Selector[T, TKey]) -> QIterable[T]: return self._lazy(lambda: ops.filtering.distinct_by(self, key_selector))

    def take(self, count: int) -> QIterable[T]: return self._lazy(lambda: ops.filtering.take(self, count))
    def take_while(self, predicate: Predicate[T]) -> QIterable[T]: return self._lazy(lambda: ops.filtering.take_while(self, predicate))
    def take_last(self, count: int) -> QIterable[T]: return self._lazy(lambda: ops.filtering.take_last(self, count))
    def skip(self, count: int) -> QIterable[T]: return self._lazy(lambda: ops.filtering.skip(self, count))
    def skip_last(self, count: int) -> QIterable[T]: return self._lazy(lambda: ops.filtering.skip_last(self, count))

    def of_type[TResult](self, target_type: type[TResult]) -> QIterable[TResult]: return C.lazy_iterable(lambda: ops.filtering.of_type(self, target_type))

    # endregion

    # region value queries
    def qcount(self, predicate: Predicate[T] | None = None) -> int: return ops.scalars.count(self, predicate)
    def none(self, predicate: Predicate[T] | None = None) -> bool: return not ops.scalars.any(self, predicate)
    def any(self, predicate: Predicate[T] | None = None) -> bool: return ops.scalars.any(self, predicate)
    def all(self, predicate: Predicate[T]) -> bool: return ops.scalars.all(self, predicate)

    # endregion

    # region sorting
    def _order_by(self, key_selector: Selector[T, SupportsRichComparison], descending: bool) -> QOrderedIterable[T]:
        return C.ordered_iterable(lambda: self, [SortInstruction(key_selector, descending)])

    def order_by(self, key_selector: Selector[T, SupportsRichComparison]) -> QOrderedIterable[T]:
        return self._order_by(key_selector, False)
    def order_by_descending(self, key_selector: Selector[T, SupportsRichComparison]) -> QOrderedIterable[T]:
        return self._order_by(key_selector, True)

    def reversed(self) -> QIterable[T]: return self._lazy(lambda: ops.ordering.reverse_lazy(self))

    def ordered(self) -> QIterable[T]: return self._lazy(lambda: ops.ordering.ordered(self))  # pyright: ignore [reportUnknownVariableType, reportArgumentType, reportUnknownLambdaType]
    # endregion

    # region mapping/transformation methods
    def select[TReturn](self, selector: Selector[T, TReturn]) -> QIterable[TReturn]: return ops.transforms.select(self, selector)
    def select_many[TInner](self, selector: Selector[T, Iterable[TInner]]) -> QIterable[TInner]: return ops.transforms.select_many(self, selector)
    def join[TInner, TKey, TResult](self, other: Iterable[TInner], self_key: Selector[T, TKey], other_key: Selector[TInner, TKey], select: Callable[[T, TInner], TResult]) -> QIterable[TResult]: return ops.transforms.join(self, other, self_key, other_key, select)

    def zip[T2, TResult](self, second: Iterable[T2], select: Callable[[T, T2], TResult]) -> QIterable[TResult]:
        return ops.zip.zip(self, second, select)

    def zip2[T2, T3, TResult](self, second: Iterable[T2], third: Iterable[T3], select: Callable[[T, T2, T3], TResult]) -> QIterable[TResult]:
        return ops.zip.zip2(self, second, third, select)

    def zip3[T2, T3, T4, TResult](self, second: Iterable[T2], third: Iterable[T3], fourth: Iterable[T4], select: Callable[[T, T2, T3, T4], TResult]) -> QIterable[TResult]:
        return ops.zip.zip3(self, second, third, fourth, select)

    @overload
    def to_dict[TKey, TValue](self, key_selector: Selector[T, TKey], value_selector: Selector[T, TValue]) -> QDict[TKey, TValue]:
        """Creates a QDict from the sequence using the specified key and value selectors"""
    @overload
    def to_dict[TKey, TValue](self: QIterable[tuple[TKey, TValue]]) -> QDict[TKey, TValue]:
        """Creates a QDict from a sequence of key-value tuples"""
    def to_dict[TKey, TValue](self, key_selector: Selector[T, TKey] | None = None, value_selector: Selector[T, TValue] | None = None) -> QDict[TKey, TValue]: return ops.transforms.to_dict(self, key_selector, value_selector)

    @overload
    def group_by[TKey](self, key: Selector[T, TKey]) -> QIterable[QGrouping[TKey, T]]:
        """Groups the elements of a sequence according to the specified key selector"""

    @overload
    def group_by[TKey, TElement](self, key: Selector[T, TKey], element: Selector[T, TElement]) -> QIterable[QGrouping[TKey, TElement]]:
        """Groups the elements of a sequence according to the specified key selector and element selector"""

    def group_by[TKey, TElement](self, key: Selector[T, TKey], element: Selector[T, TElement] | None = None) -> QIterable[QGrouping[TKey, T]] | QIterable[QGrouping[TKey, TElement]]: return ops.grouping.group_by_q(self, key, element)
    # endregion

    # region single item selecting methods
    def first(self, predicate: Predicate[T] | None = None) -> T: return ops.single_elements.first(self, predicate)
    def first_or_none(self, predicate: Predicate[T] | None = None) -> T | None: return ops.single_elements.first_or_none(self, predicate)
    def single(self, predicate: Predicate[T] | None = None) -> T: return ops.single_elements.single(self, predicate)
    def single_or_none(self, predicate: Predicate[T] | None = None) -> T | None: return ops.single_elements.single_or_none(self, predicate)

    def element_at(self, index: int) -> T: return ops.single_elements.element_at(self, index)
    def element_at_or_none(self, index: int) -> T | None: return ops.single_elements.element_at_or_none(self, index)
    # endregion

    # region methods subclasses may want to override for perfarmonce reasons

    def _optimized_length(self) -> int: return sum(1 for _ in self)
    def _assert_not_empty(self) -> Self:
        if not self.any(): raise EmptyIterableError()
        return self

    # region factory methods
    # note: we do not "optimize" by returning self in any subclass because the contract is to create a new independent copy
    def to_list(self) -> QList[T]: return C.list_(self)
    def to_set(self) -> QSet[T]: return C.set(self)
    def to_frozenset(self) -> QFrozenSet[T]: return C.frozen_set(self)
    def to_sequence(self) -> QSequence[T]: return C.sequence(self)
    def to_built_in_list(self) -> list[T]: return list(self)

    # endregion

    @staticmethod
    def empty() -> QIterable[T]: return C.empty_iterable()
