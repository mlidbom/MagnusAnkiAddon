from __future__ import annotations

from queryablecollections.collections.q_list import QList


class QGrouping[TKey, TElement](QList[TElement]):
    """Represents a collection of objects that have a common key."""
    __slots__: tuple[str, ...] = ("key",)

    def __init__(self, values: tuple[TKey, QList[TElement]]) -> None:
        super().__init__(values[1])
        self.key: TKey = values[0]
