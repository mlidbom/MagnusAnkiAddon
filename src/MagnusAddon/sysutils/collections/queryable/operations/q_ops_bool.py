from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.collections.queryable.operations.q_ops import select

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sysutils.standard_type_aliases import Predicate

def _item_not_none(value: object) -> bool: return value is not None
def all_[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> bool:
    return not any_(self, _item_not_none)  # use named functions over lambdas where possible because: https://switowski.com/blog/map-vs-list-comprehension/

def any_[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> bool:
    if predicate is None:
        iterator = iter(self)
        try:
            next(iterator)
            return True
        except StopIteration:
            return False
    return any(select(predicate, self))
