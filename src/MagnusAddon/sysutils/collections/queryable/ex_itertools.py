from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

def single[T](iterable: Iterable[T]):
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        raise IndexError("Sequece contains no elements.") from None

    try:
        next(iterator)  # Check if there's a second element
        raise ValueError("Sequence contains more than one element")
    except StopIteration:
        return first

def single_or_none[TItem](iterable: Iterable[TItem]) -> TItem | None:
    iterator = iter(iterable)
    try:
        first = next(iterator)
    except StopIteration:
        return None

    try:
        next(iterator)  # Check if there's a second element
        raise ValueError("Sequence contains more than one element")
    except StopIteration:
        return first
