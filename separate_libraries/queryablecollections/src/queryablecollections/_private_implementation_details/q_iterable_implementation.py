from __future__ import annotations

from typing import TYPE_CHECKING, override

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


class QiterableImplementation[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("_value",)
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self._value: Iterable[TItem] = iterable

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value
