from __future__ import annotations

from typing import TYPE_CHECKING

from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable

    from _typeshed import SupportsRichComparison
    from test_q_iterable_common import QIterable

    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.q_ordered_iterable import QOrderedIterable

def reverse_lazy[TItem](self: QIterable[TItem]) -> QIterable[TItem]:
    return C.lazy_iterable(lambda: reversed(list(self)))

class SortInstruction[TItem]:
    __slots__: tuple[str, ...] = ("key_selector", "descending")
    def __init__(self, key_selector: Selector[TItem, SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Selector[TItem, SupportsRichComparison] = key_selector
        self.descending: bool = descending

def sort_by_instructions[TItem](self: Iterable[TItem], sort_instructions: list[SortInstruction[TItem]]) -> Iterable[TItem]:
    items = list(self)
    for instruction in sort_instructions:  # the official documentation recommends multiple sort passes. Unless proven to perform badly in the common usage scenarios by actual performance testing, let's keep it simple: https://docs.python.org/3/howto/sorting.html
        items.sort(key=instruction.key_selector, reverse=instruction.descending)

    yield from items

def ordered[TElement: SupportsRichComparison](self: QIterable[TElement]) -> QIterable[TElement]:
    return C.lazy_iterable(lambda: sorted(self))


def order_by[TItem](self: QIterable[TItem], key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
    return C.ordered_iterable(self, [SortInstruction(key_selector, False)])

def order_by_descending[TItem](self: QIterable[TItem], key_selector: Selector[TItem, SupportsRichComparison]) -> QOrderedIterable[TItem]:
    return C.ordered_iterable(self, [SortInstruction(key_selector, True)])