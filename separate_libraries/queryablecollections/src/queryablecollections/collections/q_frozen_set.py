from __future__ import annotations

from typing import TYPE_CHECKING, Never, override

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable

class QFrozenSet[TItem](frozenset[TItem], QIterable[TItem]):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[TItem] = ()) -> QFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @override
    def _optimized_length(self) -> int: return len(self)

    _empty_set: QFrozenSet[Never]

    @staticmethod
    @override
    def empty() -> QFrozenSet[Never]:
        return QFrozenSet._empty_set

QFrozenSet._empty_set = QFrozenSet()  # pyright: ignore [reportGeneralTypeIssues, reportPrivateUsage]
