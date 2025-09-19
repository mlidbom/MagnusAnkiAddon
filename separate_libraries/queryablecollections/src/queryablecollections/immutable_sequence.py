from __future__ import annotations

from collections.abc import Sequence
from typing import overload, override


class ImmutableSequence[TItem](Sequence[TItem]):
    def __init__(self, items: Sequence[TItem] = ()) -> None:
        self._items: Sequence[TItem] = items  # Direct reference - no copying

    @override
    def __len__(self) -> int:
        return len(self._items)

    @overload
    def __getitem__(self, index: int) -> TItem: ...

    @overload
    def __getitem__(self, index: slice) -> ImmutableSequence[TItem]: ...

    @override
    def __getitem__(self, index: int | slice) -> TItem | ImmutableSequence[TItem]:
        if isinstance(index, slice):
            return ImmutableSequence(self._items[index])
        return self._items[index]
