from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections.q_errors import ArgumentError

if TYPE_CHECKING:
    from collections.abc import Iterable

def chunk[TItem](self: Iterable[TItem], size: int) -> Iterable[list[TItem]]:
    if size <= 0:
        raise ArgumentError("Chunk size must be greater than 0")

    iterator = iter(self)
    while True:
        chunk_items = list[TItem]()
        for _ in range(size):
            try:
                chunk_items.append(next(iterator))
            except StopIteration:
                if chunk_items:
                    yield chunk_items
                return
        yield chunk_items