from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

# noinspection PyPep8Naming
from queryablecollections._private_implementation_details.q_zero_overhead_collection_contructors import ZeroImportOverheadConstructors as C

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Selector
    from queryablecollections.q_grouping import QGrouping
    from queryablecollections.q_iterable import QIterable

# pycharm is wrong. Pyright sees no problem
# noinspection PyTypeHints
def _group_by[TElement, TKey](self: Iterable[TElement], key_selector: Selector[TElement, TKey]) -> Iterable[QGrouping[TKey, TElement]]:
    """Groups the elements of a sequence according to a specified key selector function."""
    from queryablecollections.collections.q_list import QList
    groups: dict[TKey, QList[TElement]] = defaultdict(QList[TElement])

    for item in self:
        groups[key_selector(item)].append(item)

    return C.iterable(groups.items()).select(C.grouping)

# pycharm is wrong. Pyright sees no problem
# noinspection PyTypeHints
def _group_by_with_element_selector[TSourceElement, TKey, TGroupElement](self: Iterable[TSourceElement],
                                                                         key_selector: Selector[TSourceElement, TKey],
                                                                         element_selector: Selector[TSourceElement, TGroupElement]) -> Iterable[QGrouping[TKey, TGroupElement]]:
    """Groups the elements of a sequence according to key and element selector functions."""
    from queryablecollections.collections.q_list import QList
    groups: dict[TKey, QList[TGroupElement]] = defaultdict(QList[TGroupElement])

    for item in self:
        groups[key_selector(item)].append(element_selector(item))

    return C.iterable(groups.items()).select(C.grouping)

def group_by_q[TItem, TKey, TElement](self: QIterable[TItem], key: Selector[TItem, TKey], element: Selector[TItem, TElement] | None = None) -> QIterable[QGrouping[TKey, TItem]] | QIterable[QGrouping[TKey, TElement]]:
    return (C.iterable(_group_by(self, key))
            if element is None
            else C.iterable(_group_by_with_element_selector(self, key, element)))
