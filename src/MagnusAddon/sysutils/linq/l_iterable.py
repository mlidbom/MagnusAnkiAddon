from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, cast, override

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

def linq[TItem](value: Iterable[TItem]) -> LIterable[TItem]: return _LIterable(value)

class LIterable[TItem](Iterable[TItem]):
    @staticmethod
    def create(value: Iterable[TItem]) -> LIterable[TItem]: return _LIterable(value)

    @property
    def _value(self) -> Iterable[TItem]: raise NotImplementedError()

    # region filtering
    def where(self, predicate: Callable[[TItem], bool]) -> LIterable[TItem]:
        return _LIterable(item for item in self._value if predicate(item))

    def not_none(self) -> LIterable[TItem]:
        return self.where(lambda item: item is not None)
    # endregion

    def none(self, predicate: Callable[[TItem], bool] | None = None) -> bool: return not self.any(predicate)

    def any(self, predicate: Callable[[TItem], bool] | None = None) -> bool:
        if predicate is None:
            for _ in self._value: return True
            return False
        return any(predicate(item) for item in self._value)

    def select[TReturn](self, selector: Callable[[TItem], TReturn]) -> LIterable[TReturn]:
        return _LIterable(selector(item) for item in self._value)

    def length(self) -> int:
        if isinstance(self._value, list): return len(cast(list[TItem], self._value))
        return sum(1 for _ in self._value)

    def single(self, predicate: Callable[[TItem], bool] | None = None) -> TItem:
        result = self.single_or_default(predicate)
        if result is None: raise ValueError("Sequence contains no elements")
        return result

    def single_or_default(self, predicate: Callable[[TItem], bool] | None = None) -> TItem | None:
        if predicate is None:
            iterator: Iterator[TItem] = iter(self._value)
            try:
                first: TItem = next(iterator)
                try:
                    next(iterator)  # Check if there's a second item
                    raise ValueError("Sequence contains more than one element")
                except StopIteration:
                    return first
            except StopIteration:
                return None
        return self.where(predicate).single_or_default()

    # region assertions on the collection or it's values

    def assert_each(self, predicate: Callable[[TItem], bool], message: str | None = None) -> LIterable[TItem]:
        for item in self:
            if not predicate(item): raise AssertionError(message)
        return self

    def assert_on_collection(self, predicate: Callable[[LIterable[TItem]], bool], message: str | None = None) -> LIterable[TItem]:
        if not predicate(self): raise AssertionError(message)
        return self

    # endregion

    # region methods to avoid needing to manually write loops
    def for_each(self, action: Callable[[TItem], None]) -> LIterable[TItem]:
        for item in self._value: action(item)
        return self

    def for_single(self, action: Callable[[TItem], None]) -> LIterable[TItem]:
        return (self.assert_on_collection(lambda seq: seq.length() == 1)
                .for_each(action))

    def for_single_or_none(self, action: Callable[[TItem], None]) -> LIterable[TItem]:
        return (self.assert_on_collection(lambda seq: seq.length() <= 1)
                .for_each(action))
    # endregion

    # region factory methods
    def to_list(self) -> LList[TItem]: return LList(self)
    def to_set(self) -> LSet[TItem]: return LSet(self)
    def to_frozenset(self) -> LFrozenSet[TItem]: return LFrozenSet(self)

    # endregion

# region implementing classes

class _LIterable[TItem](LIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        self.__value: Iterable[TItem] = iterable

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self.__value

    @override
    def __iter__(self) -> Iterator[TItem]: yield from self._value

class LFrozenSet[TItem](frozenset[TItem], LIterable[TItem]):
    def __new__(cls, iterable: Iterable[TItem]) -> LFrozenSet[TItem]:
        return super().__new__(cls, iterable)

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self

class LSequence[TItem](Sequence[TItem], LIterable[TItem]):
    pass

class LList[TItem](list[TItem], LSequence[TItem]):  # pyright: ignore [reportIncompatibleMethodOverride] things break in fascinating ways unless list is inherited first. I'm pretty sure list implements Sequence correctly...
    def __init__(self, iterable: Iterable[TItem]) -> None:
        list.__init__(self, iterable)

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self

    @override
    def to_list(self) -> LList[TItem]: return self


class LSet[TItem](set[TItem], LIterable[TItem]):
    def __init__(self, iterable: Iterable[TItem]) -> None:
        super().__init__(iterable)

    @property
    @override
    def _value(self) -> Iterable[TItem]: return self

# endregion
