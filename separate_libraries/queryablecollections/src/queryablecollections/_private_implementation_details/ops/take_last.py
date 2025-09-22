from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable

def take_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    def take_last_implementation() -> Iterable[TItem]:
        if count <= 0: return ()
        items = list(self)
        if count >= len(items):
            return items
        return items[-count:]
    return C.lazy_iterable(take_last_implementation)
