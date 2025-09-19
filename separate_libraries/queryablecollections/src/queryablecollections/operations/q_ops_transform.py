from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.type_aliases import Selector

def concat[TItem](self: Iterable[TItem], *others: Iterable[TItem]) -> Iterable[TItem]:
    return itertools.chain(self, *others)

def select[TItem, TResult](self: Iterable[TItem], selector: Selector[TItem, TResult]) -> Iterable[TResult]:
    return map(selector, self)

def flatten[TItem](self: Iterable[Iterable[TItem]]) -> Iterable[TItem]:
    return itertools.chain.from_iterable(self)

def select_many[TItem, TSubItem](self: Iterable[TItem], selector: Selector[TItem, Iterable[TSubItem]]) -> Iterable[TSubItem]:
    return flatten(select(self, selector))
