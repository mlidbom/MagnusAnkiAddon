from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, cast, overload

if TYPE_CHECKING:

    from queryablecollections.collections.numeric.q_int_types import QIterableInt
    from queryablecollections.q_iterable import QIterable


class QAs[TItem]:
    __slots__: tuple[str, ...] = ("_iterable",)
    def __init__(self, iterable: QIterable[TItem]) -> None:
        self._iterable: QIterable[TItem] = iterable



    @overload
    def int(self: QAs[int]) -> QIterableInt: ...  # pyright: ignore [reportInconsistentOverload]


    def int(self) -> QIterableInt:
        from queryablecollections.collections.numeric.q_int_types import QIterableIntImplementation
        return QIterableIntImplementation(cast(Iterable[int], self._iterable))
