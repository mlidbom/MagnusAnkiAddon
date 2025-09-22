from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from queryablecollections.q_iterable import QIterable

def zip[T, T2, TOut](first: QIterable[T],
                     second: Iterable[T2],
                     select: Callable[[T, T2], TOut]) -> QIterable[TOut]:
    def zip_implementation() -> Iterable[TOut]:
        for (first_item, second_item) in builtins.zip(first, second, strict=False):
            yield select(first_item, second_item)
    return C.lazy_iterable(zip_implementation)


