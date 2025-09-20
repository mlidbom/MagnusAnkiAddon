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
