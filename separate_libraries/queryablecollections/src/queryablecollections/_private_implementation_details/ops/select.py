from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.q_iterable import QIterable


def select[T, TResult](self: QIterable[T], selector: Selector[T, TResult]) -> QIterable[TResult]:
    return C.lazy_iterable(lambda: map(selector, self))
