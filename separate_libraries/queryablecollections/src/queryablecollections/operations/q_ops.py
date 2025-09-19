from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from sysutils.standard_type_aliases import Func

if TYPE_CHECKING:
    from collections.abc import Iterable

    from _typeshed import SupportsRichComparison
    from queryablecollections.type_aliases import Predicate, Selector

concat = itertools.chain
select = map
distinct = dict.fromkeys
take_while = itertools.takewhile
flatten = itertools.chain.from_iterable

def reverse_lazy[TItem](self: Iterable[TItem]) -> Func[Iterable[TItem]]:
    return lambda: reversed(list(self))

class SortInstruction[TItem]:
    __slots__ = ("key_selector", "descending")
    def __init__(self, key_selector: Selector[TItem, SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Selector[TItem, SupportsRichComparison] = key_selector
        self.descending: bool = descending

def where[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> Iterable[TItem]:
    return filter(predicate, self)

def _item_not_none(value: object) -> bool: return value is not None  # pyright: ignore [reportInvalidTypeVarUse]
def where_not_none[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return where(self, _item_not_none)

def select_many[TItem, TSubItem](self: Iterable[TItem], selector: Selector[TItem, Iterable[TSubItem]]) -> Iterable[TSubItem]:
    return flatten(select(selector, self))

def sort_by_instructions[TItem](self: Iterable[TItem], sort_instructions: list[SortInstruction[TItem]]) -> Iterable[TItem]:
    items = list(self)
    for instruction in sort_instructions:  # the official documentation recommends multiple sort passes. Unless proven to perform badly in the common usage scenarios by actual performance testing, let's keep it simple: https://docs.python.org/3/howto/sorting.html
        items.sort(key=instruction.key_selector, reverse=instruction.descending)

    yield from items
