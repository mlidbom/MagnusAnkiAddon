from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from queryablecollections.autoslot_shim import SlotsABC
from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable


class QFrozenSet[TItem](frozenset[TItem], QIterable[TItem], SlotsABC):
    def __new__(cls, iterable: Iterable[TItem] = ()) -> QFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    _empty_set: QFrozenSet[TItem]
    @override
    @staticmethod
    def empty() -> QFrozenSet[TItem]:
        return cast(QFrozenSet[TItem], QFrozenSet._empty_set)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QList can serve as any QList in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost

QFrozenSet._empty_set = QFrozenSet()  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]