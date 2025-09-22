from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

def take_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    if count <= 0: return ()
    items = list(self)
    if count >= len(items):
        return items
    return items[-count:]
