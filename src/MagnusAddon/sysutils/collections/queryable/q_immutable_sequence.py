from __future__ import annotations

from typing import TYPE_CHECKING, overload, override

from sysutils.collections.immutable_sequence import ImmutableSequence
from sysutils.collections.queryable.q_sequence import QSequence

if TYPE_CHECKING:
    from collections.abc import Sequence


class QImmutableSequence[TItem](ImmutableSequence[TItem], QSequence[TItem]):
    def __init__(self, sequence: Sequence[TItem] = ()) -> None:
        super().__init__(sequence)

    @overload
    def __getitem__(self, index: int) -> TItem: ...
    @overload
    def __getitem__(self, index: slice) -> QImmutableSequence[TItem]: ...
    @override
    def __getitem__(self, index: int | slice) -> TItem | QImmutableSequence[TItem]:
        if isinstance(index, slice):
            return QImmutableSequence(super().__getitem__(index))
        return super().__getitem__(index)

QSequence._empty_sequence = QImmutableSequence()  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]