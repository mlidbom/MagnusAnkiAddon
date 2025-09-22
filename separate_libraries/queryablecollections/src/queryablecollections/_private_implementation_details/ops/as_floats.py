from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from queryablecollections.collections.numeric.q_float_types import QFloatIterable
    from queryablecollections.q_iterable import QIterable


def as_floats(self: QIterable[float]) -> QFloatIterable: return C.float_iterable(lambda: self)
