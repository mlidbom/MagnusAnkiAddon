from __future__ import annotations

import weakref
from typing import TYPE_CHECKING, Generic, TypeVar, override

from autoslot import Slots

if TYPE_CHECKING:
    from _weakref import ReferenceType

T = TypeVar("T", covariant=True)

class WeakRef(Generic[T], Slots):
    def __init__(self, obj: T) -> None:
        self._weakreference: ReferenceType[T] = weakref.ref(obj)

    @property
    def instance(self) -> T:
        instance = self._weakreference()
        if instance is None: raise ReferenceError("This WeakRef instance has been destroyed by the reference counting in python. No GC roots referencing it remain.")
        return instance
    def __call__(self) -> T: return self.instance

    @override
    def __repr__(self) -> str: return f"WeakRef: {self.instance.__repr__()}"

class WeakRefable(Slots):
    __slots__ = ["__weakref__"]  # pyright: ignore[reportUninitializedInstanceVariable, reportUnannotatedClassAttribute]
