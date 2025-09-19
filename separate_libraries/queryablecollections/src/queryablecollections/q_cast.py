from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, cast

from queryablecollections.collections.numeric.q_int_types import QIterableIntImplementation

if TYPE_CHECKING:
    from queryablecollections.collections.numeric.q_int_types import QIterableInt
    from queryablecollections.q_iterable import QIterable

def _checked_cast_int(item: object) -> int:
    if not isinstance(item, int): raise TypeError(f"Expected int, got {type(item).__name__}")
    return item

class QCast[TItem]:
    __slots__: tuple[str, ...] = ("_iterable",)
    def __init__(self, iterable: QIterable[TItem]) -> None:
        self._iterable = iterable

    @property
    def checked(self) -> QCheckedCast[TItem]:
        return QCheckedCast(self._iterable)

    def int(self) -> QIterableInt:
        from queryablecollections.collections.numeric.q_int_types import QIterableIntImplementation
        return QIterableIntImplementation(cast(Iterable[int], self._iterable))

class QCheckedCast[TItem]:
    __slots__: tuple[str, ...] = ("_iterable",)
    def __init__(self, iterable: QIterable[TItem]) -> None:
        self._iterable = iterable

    def int(self) -> QIterableInt:
        return QIterableIntImplementation(cast(Iterable[int], self._iterable.select(_checked_cast_int)))
