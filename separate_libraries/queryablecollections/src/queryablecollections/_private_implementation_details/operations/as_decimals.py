from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from decimal import Decimal

    from queryablecollections.collections.numeric.q_decimal_types import QDecimalIterable
    from queryablecollections.q_iterable import QIterable


def as_decimals(self: QIterable[Decimal]) -> QDecimalIterable: return C.decimal_iterable(lambda: self)
