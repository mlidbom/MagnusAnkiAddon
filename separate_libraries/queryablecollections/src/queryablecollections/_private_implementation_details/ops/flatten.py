from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.q_iterable import QIterable


def flatten[T](self: QIterable[Iterable[T]]) -> QIterable[T]:
    return C.lazy_iterable(lambda: itertools.chain.from_iterable(self))
