from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.type_aliases import Predicate


distinct = dict.fromkeys # highly optimized and guaranteed to keep ordering
take_while = itertools.takewhile


def where[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> Iterable[TItem]:
    return filter(predicate, self)

def _item_not_none(value: object) -> bool: return value is not None  # pyright: ignore [reportInvalidTypeVarUse]
def where_not_none[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return where(self, _item_not_none)
