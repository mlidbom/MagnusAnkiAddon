from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import cast, override

from ex_autoslot import AutoSlotsABC
from sysutils.collections.queryable.q_iterable import LazyQiterable, QIterable


class QSequence[TItem](Sequence[TItem], QIterable[TItem], ABC, AutoSlotsABC):
    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return LazyQiterable[TItem](lambda: reversed(self))

    _empty_sequence: QSequence[TItem]
    @override
    @staticmethod
    def empty() -> QSequence[TItem]:
        return cast(QSequence[TItem], QSequence._empty_sequence)  # pyright: ignore [reportGeneralTypeIssues, reportUnknownMemberType] an empty QList can serve as any QList in python since generic types are not present at runtime and this gives as such an instance at virtually zero cost
