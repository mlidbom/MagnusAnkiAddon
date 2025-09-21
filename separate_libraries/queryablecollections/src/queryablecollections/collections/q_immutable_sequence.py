from __future__ import annotations

from typing import TYPE_CHECKING, overload, override

from queryablecollections._private_implementation_details.immutable_sequence import ImmutableSequence
from queryablecollections.collections.q_sequence import QSequence

if TYPE_CHECKING:
    from collections.abc import Iterable


class QImmutableSequence[TItem](ImmutableSequence[TItem], QSequence[TItem]):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[TItem] = ()) -> None:
        super().__init__(list(iterable))

    @overload
    def __getitem__(self, index: int) -> TItem: ...
    @overload
    def __getitem__(self, index: slice) -> QImmutableSequence[TItem]: ...
    @override
    def __getitem__(self, index: int | slice) -> TItem | QImmutableSequence[TItem]:
        if isinstance(index, slice):
            return QImmutableSequence(super().__getitem__(index))
        return super().__getitem__(index)
