from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable

class QFrozenSet[TItem](frozenset[TItem], QIterable[TItem]):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[TItem] = ()) -> QFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    _empty_set: QFrozenSet[TItem]

    @staticmethod
    @override
    def empty() -> QFrozenSet[TItem]:
        return cast(QFrozenSet[TItem], QFrozenSet._empty_set)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty instance can serve as any item type in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

QFrozenSet._empty_set = QFrozenSet()  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]
