from __future__ import annotations

import itertools
from collections.abc import Iterable
from typing import TYPE_CHECKING, cast

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C
from queryablecollections.q_errors import ArgumentNoneError

if TYPE_CHECKING:
    from collections.abc import Callable
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

def qzip_2[TFirst, TSecond, TResult](first: QIterable[TFirst], second: Iterable[TSecond], selector: Callable[[TFirst, TSecond], TResult]) -> QIterable[TResult]:
    def inner_zip() -> Iterable[TResult]:
        for first_item, second_item in zip(first, second, strict=False):
            yield selector(first_item, second_item)
    return C.lazy_iterable(inner_zip)

def qzip_3[TFirst, TSecond, TThird](first: QIterable[TFirst], second: Iterable[TSecond], third: Iterable[TThird]) -> QIterable[tuple[TFirst, TSecond, TThird]]:
    def inner_zip() -> Iterable[tuple[TFirst, TSecond, TThird]]:
        yield from zip(first, second, third, strict=False)
    return C.lazy_iterable(inner_zip)

def zip_new[T, T2, T3, TResult](self: QIterable[T], second: Iterable[T2], third_or_result_selector: Iterable[T3] | Callable[[T, T2], TResult] | None = None) -> QIterable[TResult] | QIterable[tuple[T, T2]] | QIterable[tuple[T, T2, T3]]:
    if third_or_result_selector is None:
        return qzip_2(self, second, lambda first_elem, second_elem: (first_elem, second_elem))
    if callable(third_or_result_selector):
        result_selector = third_or_result_selector
        return qzip_2(self, second, result_selector)
    return qzip_3(self, second, third_or_result_selector)

def flatten[T](self: QIterable[Iterable[T]]) -> QIterable[T]:
    return C.lazy_iterable(lambda: itertools.chain.from_iterable(self))

def select_many[T, TSubItem](self: QIterable[T], selector: Selector[T, Iterable[TSubItem]]) -> QIterable[TSubItem]:
    return flatten(select(self, selector))

def to_dict[T, TKey, TValue](self: QIterable[T], key_selector: Selector[T, TKey] | None = None, value_selector: Selector[T, TValue] | None = None) -> QDict[TKey, TValue]:
    if key_selector is not None:
        if value_selector is None: raise ArgumentNoneError("value_selector")
        return C.dict((key_selector(item), value_selector(item)) for item in self)

    if value_selector is not None: raise ArgumentNoneError("key_selector")

    # Assume self is a sequence of tuples. Unless the user is working without pyright and/or ignoring the errors it will be
    return C.dict(cast(Iterable[tuple[TKey, TValue]], self))

def as_int_iterable(self: QIterable[int]) -> QIntIterable: return C.int_iterable(lambda: self)
def as_float_iterable(self: QIterable[float]) -> QFloatIterable: return C.float_iterable(lambda: self)
def as_fraction_iterable(self: QIterable[Fraction]) -> QFractionIterable: return C.fraction_iterable(lambda: self)
def as_decimal_iterable(self: QIterable[Decimal]) -> QDecimalIterable: return C.decimal_iterable(lambda: self)

def join[TOuter, TInner, TKey, TResult](
        outer: QIterable[TOuter],
        inner: Iterable[TInner],
        outer_key_selector: Selector[TOuter, TKey],
        inner_key_selector: Selector[TInner, TKey],
        result_selector: Callable[[TOuter, TInner], TResult]
) -> QIterable[TResult]:
    def inner_join() -> Iterable[TResult]:
        inner_lookup: dict[TKey, list[TInner]] = {}
        for inner_item in inner:
            key = inner_key_selector(inner_item)
            if key not in inner_lookup:
                inner_lookup[key] = []
            inner_lookup[key].append(inner_item)

        # For each outer element, find matching inner elements and yield results
        for outer_item in outer:
            outer_key = outer_key_selector(outer_item)
            if outer_key in inner_lookup:
                for inner_item in inner_lookup[outer_key]:
                    yield result_selector(outer_item, inner_item)

    return C.lazy_iterable(inner_join)
