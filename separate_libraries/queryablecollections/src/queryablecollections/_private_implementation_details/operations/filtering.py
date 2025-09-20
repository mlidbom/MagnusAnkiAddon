from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate

def distinct[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return dict.fromkeys(self)  # highly optimized and guaranteed to keep ordering

def where[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> Iterable[TItem]:
    return filter(predicate, self)

def _item_not_none(value: object) -> bool: return value is not None  # pyright: ignore [reportInvalidTypeVarUse]
def where_not_none[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return where(self, _item_not_none)

def take_while[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> Iterable[TItem]:
    return itertools.takewhile(predicate, self)

def take[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return ()
    return itertools.islice(self, count)

def take_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return ()
    items = list(self)
    if count >= len(items):
        return items
    return items[-count:]

def skip[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return self
    return itertools.islice(self, count, None)

def skip_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return self
    items = list(self)
    if count >= len(items):
        return ()
    return items[:-count]
