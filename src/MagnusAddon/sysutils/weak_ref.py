from __future__ import annotations

import weakref
from typing import TYPE_CHECKING, Generic, TypeVar

from autoslot import Slots
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from _weakref import ReferenceType

T = TypeVar("T", covariant=True)

class WeakRef(Generic[T], Slots):
    def __init__(self, obj: T) -> None:
        self._weakreference: ReferenceType[T] = weakref.ref(obj)

    @property
    def instance(self) -> T: return non_optional(self._weakreference())
    def __call__(self) -> T: return non_optional(self._weakreference())

    def __repr__(self) -> str: return f"WeakRef: {self.instance.__repr__()}"

class WeakRefable(Slots):
    __slots__ = ["__weakref__"]
