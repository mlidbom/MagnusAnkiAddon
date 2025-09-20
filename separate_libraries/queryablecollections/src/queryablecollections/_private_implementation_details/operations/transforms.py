from __future__ import annotations

import itertools
from collections.abc import Iterable
from typing import TYPE_CHECKING, cast

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C
from queryablecollections.q_errors import ArgumentNoneError

if TYPE_CHECKING:
    from collections.abc import Callable

    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.collections.q_dict import QDict
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

def to_dict[TItem, TKey, TValue](self: QIterable[TItem], key_selector: Selector[TItem, TKey] | None = None, value_selector: Selector[TItem, TValue] | None = None) -> QDict[TKey, TValue]:
    if key_selector is not None:
        if value_selector is None: raise ArgumentNoneError("value_selector")
        return C.dict((key_selector(item), value_selector(item)) for item in self)

    if value_selector is not None: raise ArgumentNoneError("key_selector")

    # Assume self is a sequence of tuples. Unless the user is working without pyright and/or ignoring the errors it will be
    return C.dict(cast(Iterable[tuple[TKey, TValue]], self))

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
