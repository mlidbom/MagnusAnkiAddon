from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from queryablecollections.operations.q_ops_transform import select

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from queryablecollections.collections.q_list import QList
    from queryablecollections.type_aliases import Selector

class QGrouping[TKey, TElement]:
    """Represents a collection of objects that have a common key."""
    __slots__: tuple[str, ...] = ("key", "elements")

    def __init__(self, values: tuple[TKey, QList[TElement]]) -> None:
        self.key: TKey = values[0]
        self.elements: QList[TElement] = values[1]

    def __iter__(self) -> Iterator[TElement]:
        return iter(self.elements)

    def __len__(self) -> int:
        return len(self.elements)

def group_by[TElement, TKey](self: Iterable[TElement], key_selector: Selector[TElement, TKey]) -> Iterable[QGrouping[TKey, TElement]]:
    """Groups the elements of a sequence according to a specified key selector function."""
    from queryablecollections.collections.q_list import QList
    groups: dict[TKey, QList[TElement]] = defaultdict(QList[TElement])

    for item in self:
        key = key_selector(item)
        groups[key].append(item)

    return select(groups.items(), QGrouping)

def group_by_with_element_selector[TSourceElement, TKey, TGroupElement](self: Iterable[TSourceElement],
                                                                        key_selector: Selector[TSourceElement, TKey],
                                                                        element_selector: Selector[TSourceElement, TGroupElement]) -> Iterable[QGrouping[TKey, TGroupElement]]:
    """Groups the elements of a sequence according to key and element selector functions."""
    from queryablecollections.collections.q_list import QList
    groups: dict[TKey, QList[TGroupElement]] = defaultdict(QList[TGroupElement])

    for item in self:
        key = key_selector(item)
        element = element_selector(item)
        groups[key].append(element)

    return select(groups.items(), QGrouping)