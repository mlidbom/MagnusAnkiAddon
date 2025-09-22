from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.operations.transforms import select

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Predicate
    from queryablecollections.q_iterable import QIterable

def all[TItem](self: QIterable[TItem], predicate: Predicate[TItem]) -> bool:
    return builtins.all(select(self, predicate))  # use named functions over lambdas where possible because: https://switowski.com/blog/map-vs-list-comprehension/

def any[TItem](self: QIterable[TItem], predicate: Predicate[TItem] | None = None) -> bool:
    if predicate:
        self = self.where(predicate)

    iterator = iter(self)
    try:
        next(iterator)
        return True  # noqa: TRY300
    except StopIteration:
        return False

def count[TItem](self: QIterable[TItem], predicate: Predicate[TItem] | None = None) -> int:
    if predicate is not None: return self.where(predicate).qcount()
    return self._optimized_length()  # pyright: ignore [reportPrivateUsage]
