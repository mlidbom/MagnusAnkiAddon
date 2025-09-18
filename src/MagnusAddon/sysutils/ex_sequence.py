"""extensions to the built in Sequence type"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.collections.linq.query_module import Q

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

def flatten[T](this: Sequence[Sequence[T]]) -> list[T]:
    return Q.flatten(this).to_built_in_list()

def remove_duplicates_while_retaining_order[T](sequence: Sequence[T]) -> list[T]:
    seen: set[object] = set()
    result: list[T] = []
    for item in sequence:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def remove_duplicates[T](sequence: Sequence[T]) -> list[T]: return list(set(sequence))

def count[T](sequence: Sequence[T], predicate: Callable[[T], bool]) -> int:
    return len([t for t in sequence if predicate(t)])
