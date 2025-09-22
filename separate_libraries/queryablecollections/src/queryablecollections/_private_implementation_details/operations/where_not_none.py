from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.operations.where import where

if TYPE_CHECKING:
    from collections.abc import Iterable



def _item_not_none(value: object) -> bool: return value is not None  # pyright: ignore [reportInvalidTypeVarUse]

def where_not_none[TItem](self: Iterable[TItem]) -> Iterable[TItem]:
    return where(self, _item_not_none)
