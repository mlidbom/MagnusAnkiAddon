from __future__ import annotations

from typing import TYPE_CHECKING, override

import queryablecollections._private_implementation_details.operations as ops
from queryablecollections._private_implementation_details.operations.ordering import SortInstruction
from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from _typeshed import SupportsRichComparison

    from queryablecollections._private_implementation_details.type_aliases import Selector


class QOrderedIterable[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("sorting_instructions", "_unsorted")
    def __init__(self, iterable: Iterable[TItem], sorting_instructions: list[SortInstruction[TItem]]) -> None:
        self.sorting_instructions: list[SortInstruction[TItem]] = sorting_instructions
        self._unsorted: Iterable[TItem] = iterable

    def then_by(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=False)])

    def then_by_descending(self, key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
        return QOrderedIterable(self._unsorted, self.sorting_instructions + [SortInstruction(key_selector, descending=True)])

    @override
    def __iter__(self) -> Iterator[TItem]: yield from ops.ordering.sort_by_instructions(self._unsorted, self.sorting_instructions)
