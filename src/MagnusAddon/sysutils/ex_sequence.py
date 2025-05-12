"""extensions to the built in Sequence type"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:
    from collections.abc import Sequence

T = TypeVar('T')
U = TypeVar('U')

def flatten(this: Sequence[Sequence[T]]) -> list[T]:
    """`returns` all the items in `this` in order, flattened into a one dimensional list"""
    return [item for sub_list in this for item in sub_list]

def remove_duplicates_while_retaining_order(sequence: Sequence[T]) -> list[T]:
    seen = set()
    result = []
    for item in sequence:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def remove_duplicates(sequence: Sequence[T]) -> list[T]: return list(set(sequence))

def count(sequence: Sequence[T], predicate: Callable[[T], bool]) -> int:
    return len([t for t in sequence if predicate(t)])

class ExSequence:
    @staticmethod
    def filter(value: Sequence[T], predicate: Callable[[T], bool], invert_condition: bool = False) -> list[T]:
        return [item for item in value if predicate(item)] if not invert_condition else [item for item in value if not predicate(item)]

    @staticmethod
    def transform(value: Sequence[T], transform: Callable[[T], U]) -> list[U]:
        return [transform(item) for item in value]
