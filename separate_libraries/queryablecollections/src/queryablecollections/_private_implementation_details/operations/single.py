from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.operations.where import where
from queryablecollections.q_errors import EmptyIterableError, InvalidOperationError

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate


def single[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> TItem:
    if predicate is not None:
        self = where(self, predicate)
    iterator = iter(self)
    try:
        first_element = next(iterator)
    except StopIteration:
        raise EmptyIterableError() from None

    try:
        next(iterator)  # Check if there's a second element
        raise InvalidOperationError("Sequence contains more than one element")
    except StopIteration:
        return first_element
