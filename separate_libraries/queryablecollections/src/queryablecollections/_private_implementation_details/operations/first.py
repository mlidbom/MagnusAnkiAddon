from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.operations.where import where
from queryablecollections.q_errors import EmptyIterableError

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate


def first[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> TItem:
    if predicate is not None:
        self = where(self, predicate)
    try:
        return next(iter(self))
    except StopIteration:
        raise EmptyIterableError() from None
