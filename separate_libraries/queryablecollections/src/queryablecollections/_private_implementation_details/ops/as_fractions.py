from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from fractions import Fraction

    from queryablecollections.collections.numeric.q_fraction_types import QFractionIterable
    from queryablecollections.q_iterable import QIterable


def as_fractions(self: QIterable[Fraction]) -> QFractionIterable: return C.fraction_iterable(lambda: self)
