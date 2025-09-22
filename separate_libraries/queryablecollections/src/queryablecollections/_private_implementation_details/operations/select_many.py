from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details import operations as ops

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.q_iterable import QIterable


def select_many[T, TSubItem](self: QIterable[T], selector: Selector[T, Iterable[TSubItem]]) -> QIterable[TSubItem]:
    return ops.flatten(ops.select(self, selector))
