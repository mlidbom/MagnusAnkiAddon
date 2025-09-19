from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from _typeshed import SupportsRichComparison
    from sysutils.standard_type_aliases import Func

    from queryablecollections.type_aliases import Selector

def reverse_lazy[TItem](self: Iterable[TItem]) -> Func[Iterable[TItem]]:
    return lambda: reversed(list(self))

class SortInstruction[TItem]:
    __slots__ = ("key_selector", "descending")
    def __init__(self, key_selector: Selector[TItem, SupportsRichComparison], descending: bool) -> None:
        self.key_selector: Selector[TItem, SupportsRichComparison] = key_selector
        self.descending: bool = descending

def sort_by_instructions[TItem](self: Iterable[TItem], sort_instructions: list[SortInstruction[TItem]]) -> Iterable[TItem]:
    items = list(self)
    for instruction in sort_instructions:  # the official documentation recommends multiple sort passes. Unless proven to perform badly in the common usage scenarios by actual performance testing, let's keep it simple: https://docs.python.org/3/howto/sorting.html
        items.sort(key=instruction.key_selector, reverse=instruction.descending)

    yield from items
