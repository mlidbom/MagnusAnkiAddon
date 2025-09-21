from __future__ import annotations

from typing import TYPE_CHECKING, override

from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from queryablecollections._private_implementation_details.type_aliases import Func


class QLazyIterableImplementation[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("_factory",)
    def __init__(self, iterable_factory: Func[Iterable[TItem]]) -> None:
        self._factory: Func[Iterable[TItem]] = iterable_factory

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._factory()

class QCachingIterableImplementation[TItem](QIterable[TItem]):
    __slots__: tuple[str, ...] = ("_iterable",)
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self._iterable: Iterable[TItem] = iterable

    @override
    def __iter__(self) -> Iterator[TItem]:
        yield from iter(self._iterable)
