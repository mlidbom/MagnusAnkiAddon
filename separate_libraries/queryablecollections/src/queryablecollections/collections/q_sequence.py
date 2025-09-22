from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import Never, override

from queryablecollections._private_implementation_details.q_lazy_iterable import QLazyIterableImplementation
from queryablecollections.q_iterable import QIterable


class QSequence[TItem](Sequence[TItem], QIterable[TItem], ABC):
    __slots__: tuple[str, ...] = ()
    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return QLazyIterableImplementation[TItem](lambda: reversed(self))

    @staticmethod
    @override
    def empty() -> QSequence[Never]:
        from queryablecollections.collections.q_immutable_sequence import QImmutableSequence
        empty = QImmutableSequence[Never]()
        def get_empty() -> QSequence[Never]: return empty
        QSequence.empty = get_empty
        return QSequence[TItem].empty()
