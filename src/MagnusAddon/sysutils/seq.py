from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

class Seq[TItem]:
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self._iterable = iterable

    def where(self, predicate: Callable[[TItem], bool]) -> Seq[TItem]:
        return Seq(item for item in self._iterable if predicate(item))

    def select[TReturn](self, selector: Callable[[TItem], TReturn]) -> Seq[TReturn]:
        return Seq(selector(item) for item in self._iterable)

    def count(self) -> int:
        if isinstance(self._iterable, list): return len(self._iterable)
        return sum(1 for _ in self._iterable)

    def to_list(self) -> Sequence[TItem]:
        if isinstance(self._iterable, list): return self._iterable
        return list(self._iterable)

    def single(self, predicate: Callable[[TItem], bool] | None = None) -> TItem:
        if predicate is None:
            iterator = iter(self._iterable)
            try:
                first = next(iterator)
                try:
                    next(iterator)  # Check if there's a second item
                    raise ValueError("Sequence contains more than one element")
                except StopIteration:
                    return first
            except StopIteration:
                raise ValueError("Sequence contains no elements")  # noqa: B904
        return self.where(predicate).single()

    def for_each(self, action: Callable[[TItem], None]) -> Seq[TItem]:
        for item in self._iterable: action(item)
        return self
