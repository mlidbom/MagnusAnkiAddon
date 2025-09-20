from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from queryablecollections.operations.q_ops_transform import select

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections.q_grouping import QGrouping
    from queryablecollections.type_aliases import Selector

# pycharm is wrong. Pyright sees no problem
# noinspection PyTypeHints
def group_by[TElement, TKey](self: Iterable[TElement], key_selector: Selector[TElement, TKey]) -> Iterable[QGrouping[TKey, TElement]]:
    """Groups the elements of a sequence according to a specified key selector function."""
    from queryablecollections.collections.q_list import QList
    from queryablecollections.q_grouping import QGrouping
    groups: dict[TKey, QList[TElement]] = defaultdict(QList[TElement])

    for item in self:
        groups[key_selector(item)].append(item)

    return select(groups.items(), QGrouping)

# pycharm is wrong. Pyright sees no problem
# noinspection PyTypeHints
def group_by_with_element_selector[TSourceElement, TKey, TGroupElement](self: Iterable[TSourceElement],
                                                                        key_selector: Selector[TSourceElement, TKey],
                                                                        element_selector: Selector[TSourceElement, TGroupElement]) -> Iterable[QGrouping[TKey, TGroupElement]]:
    """Groups the elements of a sequence according to key and element selector functions."""
    from queryablecollections.collections.q_list import QList
    from queryablecollections.q_grouping import QGrouping
    groups: dict[TKey, QList[TGroupElement]] = defaultdict(QList[TGroupElement])

    for item in self:
        groups[key_selector(item)].append(element_selector(item))

    return select(groups.items(), QGrouping)