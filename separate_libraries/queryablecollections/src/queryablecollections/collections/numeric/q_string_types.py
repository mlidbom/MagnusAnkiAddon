from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, override

from queryablecollections._private_implementation_details.q_lazy_iterable import QIterableImplementation
from queryablecollections.collections.q_frozen_set import QFrozenSet
from queryablecollections.collections.q_list import QList
from queryablecollections.collections.q_sequence import QImmutableSequence
from queryablecollections.collections.q_set import QSet
from queryablecollections.q_iterable import QIterable

if TYPE_CHECKING:
    from collections.abc import Iterable

    from queryablecollections._private_implementation_details.type_aliases import Func

class QStrIterable(QIterable[str], ABC):
    __slots__: tuple[str, ...] = ()

    @override
    def to_list(self) -> QStrList: return QStrList(self)
    @override
    def to_sequence(self) -> QStrSequence: return QStrSequence(self)
    @override
    def to_set(self) -> QStrSet: return QStrSet(self)
    @override
    def to_frozenset(self) -> QStrFrozenSet: return QStrFrozenSet(self)

    def join_str(self, separator: str) -> str:
        return separator.join(self)

class QStrIterableImplementation(QIterableImplementation[str], QStrIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, factory: Func[Iterable[str]]) -> None:
        super().__init__(factory)

class QStrList(QList[str], QStrIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[str] = ()) -> None:
        super().__init__(iterable)

class QStrSet(QSet[str], QStrIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[str] = ()) -> None:
        super().__init__(iterable)

class QStrFrozenSet(QFrozenSet[str], QStrIterable):
    __slots__: tuple[str, ...] = ()
    def __new__(cls, iterable: Iterable[str] = ()) -> QStrFrozenSet:
        return super().__new__(cls, iterable)  # pyright: ignore [reportReturnType]

class QStrSequence(QImmutableSequence[str], QStrIterable):
    __slots__: tuple[str, ...] = ()
    def __init__(self, iterable: Iterable[str] = ()) -> None:
        super().__init__(iterable)
