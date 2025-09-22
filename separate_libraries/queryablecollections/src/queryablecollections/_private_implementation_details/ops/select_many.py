from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details import ops as ops

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Selector


def select_many[T, TSubItem](self: Iterable[T], selector: Selector[T, Iterable[TSubItem]]) -> Iterable[TSubItem]:
    return ops.flatten(ops.select(self, selector))
