from __future__ import annotations

from typing import TYPE_CHECKING, override

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable


class QSet[TItem](set[TItem], QIterable[TItem]):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def contains(self, value: TItem) -> bool: return value in self