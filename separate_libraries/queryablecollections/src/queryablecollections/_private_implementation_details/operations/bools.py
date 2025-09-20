from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.operations.transforms import select

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate

def all_[TItem](self: Iterable[TItem], predicate: Predicate[TItem]) -> bool:
    return all(select(self, predicate))  # use named functions over lambdas where possible because: https://switowski.com/blog/map-vs-list-comprehension/

def any_[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> bool:
    if predicate is None:
        iterator = iter(self)
        try:
            next(iterator)
            return True  # noqa: TRY300
        except StopIteration:
            return False
    return any(select(self, predicate, ))
