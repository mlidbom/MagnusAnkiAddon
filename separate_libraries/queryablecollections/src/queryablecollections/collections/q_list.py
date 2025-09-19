from __future__ import annotations

import sys
from typing import TYPE_CHECKING, SupportsIndex, overload, override

from queryablecollections.collections.q_sequence import QSequence
from queryablecollections.q_iterable import QLazyiterable, QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable

class QList[TItem](list[TItem], QSequence[TItem], QIterable[TItem]):
    __slots__ = ()
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return QLazyiterable[TItem](lambda: reversed(self))

    @override
    def element_at(self, index: int) -> TItem: return self[index]

    @override
    def index(self, value: TItem, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize) -> int:
        return super().index(value, start, stop)

    @override
    def count(self, value: TItem): return super().count(value)

    @overload
    def __getitem__(self, index: SupportsIndex) -> TItem: ...

    @overload
    def __getitem__(self, index: slice) -> QList[TItem]: ...

    @override
    def __getitem__(self, index: SupportsIndex | slice) -> TItem | QList[TItem]:
        if isinstance(index, slice):
            return QList(super().__getitem__(index))
        return super().__getitem__(index)

    @staticmethod
    @override
    def empty() -> QList[TItem]: return QList()  # QList is mutable, so unlike our base types we cannot reuse an instance
