from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.q_iterable import QIterable

def concat[TItem](self: QIterable[TItem], *others: Iterable[TItem]) -> QIterable[TItem]:
    return C.iterable(itertools.chain(self, *others))

def select[TItem, TResult](self: QIterable[TItem], selector: Selector[TItem, TResult]) -> QIterable[TResult]:
    return C.iterable(map(selector, self))

def zip_with_selector[TFirst, TSecond, TResult](first: QIterable[TFirst], second: Iterable[TSecond], selector: Callable[[TFirst, TSecond], TResult]) -> QIterable[TResult]:
    def inner_zip() -> Iterable[TResult]:
        for first_item, second_item in zip(first, second, strict=False):
            yield selector(first_item, second_item)
    return C.lazy_iterable(inner_zip)

def flatten[TItem](self: QIterable[Iterable[TItem]]) -> QIterable[TItem]:
    return C.iterable(itertools.chain.from_iterable(self))

def select_many[TItem, TSubItem](self: QIterable[TItem], selector: Selector[TItem, Iterable[TSubItem]]) -> QIterable[TSubItem]:
    return flatten(select(self, selector))

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
