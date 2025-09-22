from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from decimal import Decimal
    from fractions import Fraction

    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.collections.numeric.q_decimal_types import QDecimalIterable
    from queryablecollections.collections.numeric.q_float_types import QFloatIterable
    from queryablecollections.collections.numeric.q_fraction_types import QFractionIterable
    from queryablecollections.collections.numeric.q_int_types import QIntIterable
    from queryablecollections.collections.q_dict import QDict
    from queryablecollections.q_iterable import QIterable

def concat[T](self: Iterable[T], *others: Iterable[T]) -> Iterable[T]:
    return itertools.chain(self, *others)

def select[T, TResult](self: QIterable[T], selector: Selector[T, TResult]) -> QIterable[TResult]:
    return C.lazy_iterable(lambda: map(selector, self))

def flatten[T](self: QIterable[Iterable[T]]) -> QIterable[T]:
    return C.lazy_iterable(lambda: itertools.chain.from_iterable(self))

def select_many[T, TSubItem](self: QIterable[T], selector: Selector[T, Iterable[TSubItem]]) -> QIterable[TSubItem]:
    return flatten(select(self, selector))

def to_dict[T, TKey, TValue](self: QIterable[T], key_selector: Selector[T, TKey], value_selector: Selector[T, TValue]) -> QDict[TKey, TValue]:
    return C.dict((key_selector(item), value_selector(item)) for item in self)

def as_ints(self: QIterable[int]) -> QIntIterable: return C.int_iterable(lambda: self)
def as_floats(self: QIterable[float]) -> QFloatIterable: return C.float_iterable(lambda: self)
def as_fractions(self: QIterable[Fraction]) -> QFractionIterable: return C.fraction_iterable(lambda: self)
def as_decimals(self: QIterable[Decimal]) -> QDecimalIterable: return C.decimal_iterable(lambda: self)

def join[TOuter, TInner, TKey, TResult](
        first: QIterable[TOuter],
        second: Iterable[TInner],
        first_key: Selector[TOuter, TKey],
        second_key: Selector[TInner, TKey],
        select: Callable[[TOuter, TInner], TResult]
) -> QIterable[TResult]:
    def inner_join() -> Iterable[TResult]:
        inner_lookup: dict[TKey, list[TInner]] = {}
        for inner_item in second:
            key = second_key(inner_item)
            if key not in inner_lookup:
                inner_lookup[key] = []
            inner_lookup[key].append(inner_item)

        # For each outer element, find matching inner elements and yield results
        for outer_item in first:
            outer_key = first_key(outer_item)
            if outer_key in inner_lookup:
                for inner_item in inner_lookup[outer_key]:
                    yield select(outer_item, inner_item)

    return C.lazy_iterable(inner_join)
