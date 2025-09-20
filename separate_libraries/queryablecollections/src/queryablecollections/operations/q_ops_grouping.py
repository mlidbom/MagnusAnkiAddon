from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from queryablecollections.collections.q_list import QList
    from queryablecollections.type_aliases import Selector

class QGrouping[TKey, TElement]:
    """Represents a collection of objects that have a common key."""
    __slots__: tuple[str, ...] = ("key", "elements")

    def __init__(self, key: TKey, elements: QList[TElement]) -> None:
        self.key: TKey = key
        self.elements: QList[TElement] = elements

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

    return (QGrouping(key, elements) for key, elements in groups.items())

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

    return (QGrouping(key, elements) for key, elements in groups.items())

def group_by_with_result_selector[TSourceElement, TKey, TGroupElement](self: Iterable[TSourceElement],
                                                                       key_selector: Selector[TSourceElement, TKey],
                                                                       result_selector: Selector[QGrouping[TKey, TSourceElement], TGroupElement]) -> Iterable[TGroupElement]:
    """Groups elements and projects each group using a result selector."""
    return (result_selector(group) for group in group_by(self, key_selector))

def group_by_with_element_and_result_selector[TItem, TKey, TElement, TResult](self: Iterable[TItem],
                                                                              key_selector: Selector[TItem, TKey],
                                                                              element_selector: Selector[TItem, TElement],
                                                                              result_selector: Selector[QGrouping[TKey, TElement], TResult]) -> Iterable[TResult]:
    """Groups elements with element selector and projects each group using a result selector."""
    return (result_selector(group) for group in group_by_with_element_selector(self, key_selector, element_selector))
