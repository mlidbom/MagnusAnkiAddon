from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import cast, overload, override

from queryablecollections.immutable_sequence import ImmutableSequence
from queryablecollections.q_iterable import LazyQiterable, QIterable


class QSequence[TItem](Sequence[TItem], QIterable[TItem], ABC):
    __slots__ = ()
    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return LazyQiterable[TItem](lambda: reversed(self))

    _empty_sequence: QSequence[TItem]
    @staticmethod
    @override
    def empty() -> QSequence[TItem]:
        return cast(QSequence[TItem], QSequence._empty_sequence)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QList can serve as any QList in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

class QImmutableSequence[TItem](ImmutableSequence[TItem], QSequence[TItem]):
    __slots__ = ()
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
