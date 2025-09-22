from __future__ import annotations

import builtins
from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details import ops

if TYPE_CHECKING:
    from queryablecollections._private_implementation_details.type_aliases import Predicate
    from queryablecollections.q_iterable import QIterable


def all[TItem](self: QIterable[TItem], predicate: Predicate[TItem]) -> bool:
    return builtins.all(ops.select(self, predicate))
