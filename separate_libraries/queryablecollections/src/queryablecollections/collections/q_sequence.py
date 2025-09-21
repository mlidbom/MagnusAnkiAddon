from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import override

from queryablecollections._private_implementation_details.q_lazy_iterable import QIterableImplementation
from queryablecollections.q_iterable import QIterable


class QSequence[TItem](Sequence[TItem], QIterable[TItem], ABC):
    __slots__: tuple[str, ...] = ()
    @override
    def _optimized_length(self) -> int: return len(self)

    @override
    def reversed(self) -> QIterable[TItem]: return QIterableImplementation[TItem](lambda: reversed(self))

    @staticmethod
    @override
    def empty() -> QSequence[TItem]:
        from queryablecollections.collections.q_immutable_sequence import QImmutableSequence
        empty = QImmutableSequence[TItem]()
        def get_empty() -> QSequence[TItem]: return empty
        QSequence.empty = get_empty # replace this method with get_empty so that future calls have zero overhead, just returning a reference
        return QSequence[TItem].empty() # call the new version so we know from the very first call that it works

