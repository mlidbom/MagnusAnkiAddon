from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from queryablecollections.collections.numeric.q_int_types import QIntIterable
    from queryablecollections.q_iterable import QIterable


def as_ints(self: QIterable[int]) -> QIntIterable: return C.int_iterable(lambda: self)
