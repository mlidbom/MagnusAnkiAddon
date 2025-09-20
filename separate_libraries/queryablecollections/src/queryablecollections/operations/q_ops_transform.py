from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from queryablecollections.type_aliases import Selector

def concat[TItem](self: Iterable[TItem], *others: Iterable[TItem]) -> Iterable[TItem]:
    return itertools.chain(self, *others)

def select[TItem, TResult](self: Iterable[TItem], selector: Selector[TItem, TResult]) -> Iterable[TResult]:
    return map(selector, self)

def zip_with_selector[TFirst, TSecond, TResult](first: Iterable[TFirst], second: Iterable[TSecond], selector: Callable[[TFirst, TSecond], TResult]) -> Iterable[TResult]:
    for first_item, second_item in zip(first, second, strict=False):
        yield selector(first_item, second_item)

def flatten[TItem](self: Iterable[Iterable[TItem]]) -> Iterable[TItem]:
    return itertools.chain.from_iterable(self)

def select_many[TItem, TSubItem](self: Iterable[TItem], selector: Selector[TItem, Iterable[TSubItem]]) -> Iterable[TSubItem]:
    return flatten(select(self, selector))

def join[TOuter, TInner, TKey, TResult](
        outer: Iterable[TOuter],
        inner: Iterable[TInner],
        outer_key_selector: Selector[TOuter, TKey],
        inner_key_selector: Selector[TInner, TKey],
        result_selector: Callable[[TOuter, TInner], TResult]
) -> Iterable[TResult]:
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
