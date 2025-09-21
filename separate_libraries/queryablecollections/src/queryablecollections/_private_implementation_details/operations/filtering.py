from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate, Selector
    from queryablecollections.q_iterable import QIterable

def distinct[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return dict.fromkeys(self)  # highly optimized and guaranteed to keep ordering

def distinct_by[TItem, TKey](self: Iterable[TItem], key_selector: Selector[TItem, TKey]) -> Iterable[TItem]:
    seen: dict[TKey, TItem] = {}
    for item in self:
        key = key_selector(item)
        if key not in seen:
            seen[key] = item
    return seen.values()


def where[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> Iterable[TItem]:
    return filter(predicate, self)

def _item_not_none(value: object) -> bool: return value is not None  # pyright: ignore [reportInvalidTypeVarUse]
def where_not_none[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return where(self, _item_not_none)

def take_while[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> Iterable[TItem]:
    return itertools.takewhile(predicate, self)

def take[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return C.empty_iterable()
    return itertools.islice(self, count)

def take_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    def internal_take_last() -> Iterable[TItem]:
        if count <= 0: return ()
        items = list(self)
        if count >= len(items):
            return items
        return items[-count:]
    return C.lazy_iterable(internal_take_last)


def skip[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return self
    return itertools.islice(self, count, None)

def skip_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    def internal_skip_last() -> Iterable[TItem]:
        if count <= 0: return self
        items = list(self)
        if count >= len(items):
            return C.empty_iterable()
        return items[:-count]
    return C.lazy_iterable(internal_skip_last)

class _TypeTester:
    def __init__(self, type_: type) -> None:
        self.type_:type = type_
    def __call__(self, value: object) -> bool:
        return isinstance(value, self.type_)

def of_type[TItem, TResult](self: QIterable[TItem], type_: type[TResult]) -> Iterable[TResult]:
    return self.where(_TypeTester(type_)).cast.to(type_)
