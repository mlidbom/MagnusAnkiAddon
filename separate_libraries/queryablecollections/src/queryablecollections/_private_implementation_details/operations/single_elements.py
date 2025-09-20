from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.operations.filtering import where
from queryablecollections.q_errors import EmptyIterableError, InvalidOperationError

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Predicate
    from queryablecollections.q_iterable import QIterable

def first[TItem](self: QIterable[TItem], predicate: Predicate[TItem] | None = None):
    if predicate is not None:
        self = where(self, predicate)
    try:
        return next(iter(self))
    except StopIteration:
        raise EmptyIterableError() from None

def first_or_none[TItem](self: QIterable[TItem], predicate: Predicate[TItem] | None = None) -> TItem | None:
    if predicate is not None:
        self = where(self, predicate)
    try:
        return next(iter(self))
    except StopIteration:
        return None

def single[TItem](self: QIterable[TItem], predicate: Predicate[TItem] | None = None):
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

def single_or_none[TItem](self: QIterable[TItem], predicate: Predicate[TItem] | None = None) -> TItem | None:
    if predicate is not None:
        self = where(self, predicate)
    iterator = iter(self)
    try:
        first_element = next(iterator)
    except StopIteration:
        return None

    try:
        next(iterator)  # Check if there's a second element
        raise InvalidOperationError("Sequence contains more than one element")
    except StopIteration:
        return first_element

def element_at[TItem](self: Iterable[TItem], index: int) -> TItem:
    try:
        return next(itertools.islice(self, index, index + 1))
    except StopIteration:
        raise IndexError(f"Index {index} was outside the bounds of the collection.") from None

def element_at_or_none[TItem](self: Iterable[TItem], index: int) -> TItem | None:
    return next(itertools.islice(self, index, index + 1), None)
