from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable


def skip_last[TItem](self: Iterable[TItem], count: int) -> Iterable[TItem]:
    def internal_skip_last() -> Iterable[TItem]:
        if count <= 0: return self
        items = list(self)
        if count >= len(items):
            return C.empty_iterable()
        return items[:-count]
    return C.lazy_iterable(internal_skip_last)
