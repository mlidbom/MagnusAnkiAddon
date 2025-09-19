from __future__ import annotations

from typing import TYPE_CHECKING, override

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable


class QSet[TItem](set[TItem], QIterable[TItem]):
    __slots__ = ()
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    @staticmethod
    @override
    def empty() -> QSet[TItem]: return QSet()  # QSet is mutable, so unlike our base types we cannot reuse an instance
