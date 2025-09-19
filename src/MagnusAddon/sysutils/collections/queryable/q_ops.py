from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from _typeshed import SupportsRichComparison
    from sysutils.standard_type_aliases import Predicate, Selector

concat = itertools.chain
select = map
where = filter
distinct = dict.fromkeys
take_while = itertools.takewhile
flatten = itertools.chain.from_iterable

#use named functions over lambdas where possible because: https://switowski.com/blog/map-vs-list-comprehension/
class SortInstruction[TItem]:
    def __init__(self, key_selector: Selector[TItem, SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Selector[TItem, SupportsRichComparison] = key_selector
        self.descending: bool = descending

def single[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None):
    if predicate is not None:
        self = where(predicate, self)
    iterator = iter(self)
    try:
        first = next(iterator)
    except StopIteration:
        raise IndexError("Sequece contains no elements.") from None

    try:
        next(iterator)  # Check if there's a second element
        raise ValueError("Sequence contains more than one element")
    except StopIteration:
        return first

def single_or_none[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> TItem | None:
    if predicate is not None:
        self = where(predicate, self)
    iterator = iter(self)
    try:
        first = next(iterator)
    except StopIteration:
        return None

    try:
        next(iterator)  # Check if there's a second element
        raise ValueError("Sequence contains more than one element")
    except StopIteration:
        return first

def select_many[TItem, TSubItem](self: Iterable[TItem], selector: Selector[TItem, Iterable[TSubItem]]) -> Iterable[TSubItem]:
    return flatten(select(selector, self))

def sort_by_instructions[TItem](self: Iterable[TItem], sort_instructions: list[SortInstruction[TItem]]) -> Iterable[TItem]:
    items = list(self)
    for instruction in sort_instructions: # the official documentation recommends multiple sort passes. Unless proven to perform badly in the common usage scenarios by actual performance testing, let's keep it simple: https://docs.python.org/3/howto/sorting.html
        items.sort(key=instruction.key_selector, reverse=instruction.descending)

    yield from items

def _item_not_none(value: object) -> bool: return value is not None
def none[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None ) -> bool:
    return not any_(self, _item_not_none)

def any_[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> bool:
    if predicate is None:
        iterator = iter(self)
        try:
            next(iterator)
            return True
        except StopIteration:
            return False
    return any(select(predicate, self))
