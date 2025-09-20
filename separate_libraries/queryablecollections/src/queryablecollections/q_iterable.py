from __future__ import annotations

from abc import ABC
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any, overload

import queryablecollections._private_implementation_details.operations as ops

# noinspection PyPep8Naming
from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from decimal import Decimal
    from fractions import Fraction

    from _typeshed import SupportsRichComparison

    from queryablecollections._private_implementation_details.type_aliases import Action1, Predicate, Selector
    from queryablecollections.collections.numeric.q_decimal_types import QIterableDecimal
    from queryablecollections.collections.numeric.q_float_types import QIterableFloat
    from queryablecollections.collections.numeric.q_fraction_types import QIterableFraction
    from queryablecollections.collections.numeric.q_int_types import QIterableInt
    from queryablecollections.collections.q_dict import QDict
    from queryablecollections.collections.q_frozen_set import QFrozenSet
    from queryablecollections.collections.q_list import QList
    from queryablecollections.collections.q_sequence import QSequence
    from queryablecollections.collections.q_set import QSet
    from queryablecollections.q_as import QAs
    from queryablecollections.q_cast import QCast
    from queryablecollections.q_grouping import QGrouping
    from queryablecollections.q_ordered_iterable import QOrderedIterable

def query[TItem](value: Iterable[TItem]) -> QIterable[TItem]: return C.iterable(value)

# note to coders, you can trust that the methods in QIterable do nothing except delegate to the corresponding operations method,
# or to ZeroImportOverheadConstructors, that's why we keep all the methods on single lines to make it easier to read through the definitions
class QIterable[T](Iterable[T], ABC):
    __slots__: tuple[str, ...] = ()
    @property
    def cast(self) -> QCast[T]: return C.cast(self)

    @property
    def qas(self) -> QAs[T]: return C.qas(self)

    # region operations on the whole collection, not the items
    def concat(self, *others: Iterable[T]) -> QIterable[T]: return ops.transforms.concat(self, *others)
    # endregion

    # region functional programming helpers
    def pipe_to[TReturn](self, action: Selector[QIterable[T], TReturn]) -> TReturn: return ops.functional.pipe_to(self, action)
    def for_each(self, action: Action1[T]) -> QIterable[T]: return ops.functional.for_each(self, action)
    def for_single(self, action: Selector[T, Any]) -> QIterable[T]:  return ops.functional.for_single(self, action)  # pyright: ignore[reportExplicitAny]
    def for_single_or_none(self, action: Selector[T, Any]) -> QIterable[T]: return ops.functional.for_single_or_none(self, action)  # pyright: ignore[reportExplicitAny]
    # endregion


    # region typed convertions to access type specific functionality

    @overload
    def as_int(self: QIterable[int]) -> QIterableInt: ...  # pyright: ignore [reportInconsistentOverload]
    def as_int(self) -> QIterableInt: return self.cast.int()

    @overload
    def as_float(self: QIterable[float]) -> QIterableFloat: ...  # pyright: ignore [reportInconsistentOverload]
    def as_float(self) -> QIterableFloat: return self.cast.float()

    @overload
    def as_fraction(self: QIterable[Fraction]) -> QIterableFraction: ...  # pyright: ignore [reportInconsistentOverload]
    def as_fraction(self) -> QIterableFraction: return self.cast.fraction()

    @overload
    def as_decimal(self: QIterable[Decimal]) -> QIterableDecimal: ...  # pyright: ignore [reportInconsistentOverload]
    def as_decimal(self) -> QIterableDecimal: return self.cast.decimal()

    #endregion

    # region filtering
    def where(self, predicate: Predicate[T]) -> QIterable[T]: return ops.filtering.where(self, predicate)
    def where_not_none(self) -> QIterable[T]: return ops.filtering.where_not_none(self)

    def distinct(self) -> QIterable[T]: return ops.filtering.distinct(self)

    def take_while(self, predicate: Predicate[T]) -> QIterable[T]: return ops.filtering.take_while(self, predicate)
    def take(self, count: int) -> QIterable[T]: return ops.filtering.take(self, count)
    def take_last(self, count: int) -> QIterable[T]: return ops.filtering.take_last(self, count)
    def skip(self, count: int) -> QIterable[T]: return ops.filtering.skip(self, count)
    def skip_last(self, count: int) -> QIterable[T]: return ops.filtering.skip_last(self, count)

    def of_type[TResult](self, target_type: type[TResult]) -> QIterable[TResult]: return ops.filtering.of_type(self, target_type)

    # endregion

    # region value queries
    def qcount(self, predicate: Predicate[T] | None = None) -> int: return ops.scalars.count(self, predicate)
    def none(self, predicate: Predicate[T] | None = None) -> bool: return not ops.scalars.any_(self, predicate)
    def any(self, predicate: Predicate[T] | None = None) -> bool: return ops.scalars.any_(self, predicate)
    def all(self, predicate: Predicate[T]) -> bool: return ops.scalars.all_(self, predicate)

    # endregion

    # region sorting
    def order_by(self, key_selector: Selector[T, SupportsRichComparison]) -> QOrderedIterable[T]: return ops.ordering.order_by(self, key_selector)
    def order_by_descending(self, key_selector: Selector[T, SupportsRichComparison]) -> QOrderedIterable[T]: return ops.ordering.order_by_descending(self, key_selector)

    def reversed(self) -> QIterable[T]: return ops.ordering.reverse_lazy(self)

    def ordered(self) -> QIterable[T]: return ops.ordering.ordered(self)  # pyright: ignore [reportUnknownVariableType, reportArgumentType]
    # endregion

    # region mapping/transformation methods
    def select[TReturn](self, selector: Selector[T, TReturn]) -> QIterable[TReturn]: return ops.transforms.select(self, selector)
    def select_many[TInner](self, selector: Selector[T, Iterable[TInner]]) -> QIterable[TInner]: return ops.transforms.select_many(self, selector)
    def join[TInner, TKey, TResult](self, inner: Iterable[TInner], outer_key: Selector[T, TKey], inner_key: Selector[TInner, TKey], result: Callable[[T, TInner], TResult]) -> QIterable[TResult]: return ops.transforms.join(self, inner, outer_key, inner_key, result)

    @overload
    def zip[T2, TResult](self, second: Iterable[T2], result_selector: Callable[[T, T2], TResult], /) -> QIterable[TResult]: ...

    @overload
    def zip[T2](self, second: Iterable[T2], /) -> QIterable[tuple[T, T2]]: ...

    @overload
    def zip[T2, T3](self, second: Iterable[T2], third: Iterable[T3], /) -> QIterable[tuple[T, T2, T3]]: ...

    def zip[T2, T3, TResult](self, second: Iterable[T2], third: Iterable[T3] | Callable[[T, T2], TResult] | None = None) \
            -> QIterable[TResult] | QIterable[tuple[T, T2]] | QIterable[tuple[T, T2, T3]]:
        return ops.transforms.zip_new(self, second, third)

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

    # region assertions on the collection or it's values
    def assert_each(self, predicate: Predicate[T], message: str | Selector[T, str] | None = None) -> QIterable[T]: return ops.asserts.each_element(self, predicate, message)
    def assert_on_collection(self, predicate: Predicate[QIterable[T]], message: str | None = None) -> QIterable[T]: return ops.asserts.collection(self, predicate, message)
    # endregion

    # region methods subclasses may want to override for perfarmonce reasons

    def _optimized_length(self) -> int: return sum(1 for _ in self)
    def _assert_not_empty(self) -> QIterable[T]: return ops.asserts.not_empty(self)

    # region factory methods
    # note: we do not "optimize" by returning self in any subclass because the contract is to create a new independent copy
    def to_list(self) -> QList[T]: return C.list(self)
    def to_set(self) -> QSet[T]: return C.set(self)
    def to_frozenset(self) -> QFrozenSet[T]: return C.frozen_set(self)
    def to_sequence(self) -> QSequence[T]: return C.sequence(self)
    def to_built_in_list(self) -> list[T]: return list(self)

    # endregion

    @staticmethod
    def empty() -> QIterable[T]: return C.empty_iterable()
