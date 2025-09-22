from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from _typeshed import SupportsRichComparison

    from queryablecollections._private_implementation_details.type_aliases import Selector


class SortInstruction[TItem]:
    __slots__: tuple[str, ...] = ("key_selector", "descending")
    def __init__(self, key_selector: Selector[TItem, SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Selector[TItem, SupportsRichComparison] = key_selector
        self.descending: bool = descending
