from __future__ import annotations

import weakref
from typing import TYPE_CHECKING, Generic, TypeVar, override

from ex_autoslot import ProfilableAutoSlots

if TYPE_CHECKING:
    from _weakref import ReferenceType

T = TypeVar("T", covariant=True)

class WeakRef(Generic[T], ProfilableAutoSlots):  # noqa: UP046 the automatic inference thinks this in invariant even though it is covariant so we need the old syntax
    def __init__(self, obj: T) -> None:
        self._weakreference: ReferenceType[T] = weakref.ref(obj)

    def _weakref_get_instance(self) -> T:
        instance = self._weakreference()
        if instance is None: raise ReferenceError("This WeakRef instance has been destroyed by the reference counting in python. No GC roots referencing it remain.")
        return instance

    def __call__(self) -> T: return self._weakref_get_instance()

    @override
    def __repr__(self) -> str: return f"WeakRef: {self().__repr__()}"

class WeakRefable(ProfilableAutoSlots):
    __slots__ = ["__weakref__"]  # pyright: ignore[reportUninitializedInstanceVariable, reportUnannotatedClassAttribute]
