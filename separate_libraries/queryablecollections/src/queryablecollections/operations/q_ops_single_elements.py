from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections.operations.q_ops import where

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.type_aliases import Predicate

def single[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None):
    if predicate is not None:
        self = where(self, predicate)
    iterator = iter(self)
    try:
        first = next(iterator)
    except StopIteration:
        raise IndexError("Sequece contains no elements.") from None

    try:
        next(iterator)  # Check if there's a second element
        raise ValueError("Sequence contains more than one element")
    except StopIteration:
        return first

def single_or_none[TItem](self: Iterable[TItem], predicate: Predicate[TItem] | None = None) -> TItem | None:
    if predicate is not None:
        self = where(self, predicate)
    iterator = iter(self)
    try:
        first = next(iterator)
    except StopIteration:
        return None

    try:
        next(iterator)  # Check if there's a second element
        raise ValueError("Sequence contains more than one element")
    except StopIteration:
        return first

def element_at[TItem](self: Iterable[TItem], index: int) -> TItem:
    try:
        return next(itertools.islice(self, index, index + 1))
    except StopIteration:
        raise IndexError(f"Index {index} was outside the bounds of the collection.") from None

def element_at_or_none[TItem](self: Iterable[TItem], index: int) -> TItem | None:
    return next(itertools.islice(self, index, index + 1), None)
