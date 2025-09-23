from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from queryablecollections.collections.numeric.q_int_types import QIntIterable

def range(start_or_stop: int, stop: int | None = None, step: int = 1, /) -> QIntIterable:
    if stop is None:
        start = 0
        stop = start_or_stop
    else:
        start = start_or_stop

    return C.int_iterable(lambda: range(start, stop, step))
