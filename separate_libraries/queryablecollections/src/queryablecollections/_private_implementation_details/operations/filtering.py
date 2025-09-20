from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate
    from queryablecollections.q_iterable import QIterable

def distinct[TItem](self: QIterable[TItem]) -> QIterable[TItem]:
    return C.lazy_iterable(lambda: dict.fromkeys(self))  # highly optimized and guaranteed to keep ordering

def where[TItem](self: QIterable[TItem], predicate: Predicate[TItem]) -> QIterable[TItem]:
    return C.iterable(filter(predicate, self))

def _item_not_none(value: object) -> bool: return value is not None  # pyright: ignore [reportInvalidTypeVarUse]
def where_not_none[TItem](self: QIterable[TItem]) -> QIterable[TItem]:
    return C.iterable(where(self, _item_not_none))

def take_while[TItem](self: QIterable[TItem], predicate: Predicate[TItem]) -> QIterable[TItem]:
    return C.iterable(itertools.takewhile(predicate, self))

def take[TItem](self: QIterable[TItem], count: int) -> QIterable[TItem]:
    if count <= 0: return C.empty_iterable()
    return C.iterable(itertools.islice(self, count))

def take_last[TItem](self: QIterable[TItem], count: int) -> QIterable[TItem]:
    def internal_take_last() -> Iterable[TItem]:
        if count <= 0: return ()
        items = list(self)
        if count >= len(items):
            return items
        return items[-count:]
    return C.lazy_iterable(internal_take_last)


def skip[TItem](self: QIterable[TItem], count: int) -> QIterable[TItem]:
    if count <= 0: return self
    return C.iterable(itertools.islice(self, count, None))

def skip_last[TItem](self: QIterable[TItem], count: int) -> QIterable[TItem]:
    def internal_skip_last() -> Iterable[TItem]:
        if count <= 0: return self
        items = list(self)
        if count >= len(items):
            return C.empty_iterable()
        return items[:-count]
    return C.lazy_iterable(internal_skip_last)
