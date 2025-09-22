from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from queryablecollections.q_iterable import QIterable


def zip3[T, T2, T3, T4, TOut](first: QIterable[T],
                              second: Iterable[T2],
                              third: Iterable[T3],
                              fourth: Iterable[T4],
                              select: Callable[[T, T2, T3, T4], TOut]) -> QIterable[TOut]:
    def zip3_implementation() -> Iterable[TOut]:
        for first_item, second_item, third_item, fourth_item in builtins.zip(first, second, third, fourth, strict=False):
            yield select(first_item, second_item, third_item, fourth_item)
    return C.lazy_iterable(zip3_implementation)
