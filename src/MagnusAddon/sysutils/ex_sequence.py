"""extensions to the built in Sequence type"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

def remove_duplicates_while_retaining_order[T](sequence: Sequence[T]) -> list[T]:
    seen: set[object] = set()
    result: list[T] = []
    for item in sequence:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

